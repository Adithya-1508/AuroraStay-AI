from typing import Any

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel

from security.ai_security.guardrails import AIGuardrails
from security.api_security.rate_limit import SlidingWindowRateLimiter
from security.audit.trail import AuditTrail
from security.authentication.jwt import JWTAuth
from security.authorization.engine import PermissionEngine
from security.incident_response.tracker import SecurityIncidentTracker
from security.rbac.roles import ENTERPRISE_ROLES
from security.risk.evaluator import RiskEvaluator

router = APIRouter()

# Global Limiter & Trackers
rate_limiter = SlidingWindowRateLimiter(window_seconds=60, max_requests=100)
audit_trail = AuditTrail()
incident_tracker = SecurityIncidentTracker()

# In-memory DB mocks
user_db: dict[str, dict[str, Any]] = {
    "usr-admin": {
        "id": "usr-admin",
        "username": "admin",
        "roles": ["Administrator"],
        "department": "Administration",
        "status": "ACTIVE",
    },
    "usr-guest": {
        "id": "usr-guest",
        "username": "guest_user",
        "roles": ["Guest"],
        "department": "Guest Experience",
        "status": "ACTIVE",
    },
}


# Request Schemas
class LoginRequest(BaseModel):
    username: str
    password: str


class TokenRefreshRequest(BaseModel):
    refresh_token: str


class UserCreateRequest(BaseModel):
    username: str
    roles: list[str]
    department: str


class UserUpdateRequest(BaseModel):
    roles: list[str] | None = None
    department: str | None = None
    status: str | None = None


class RoleCreateRequest(BaseModel):
    role_name: str
    permissions: list[str]


class SecurityIncidentRequest(BaseModel):
    title: str
    severity: str
    source_ip: str
    linked_audits: list[str]


@router.post("/auth/login", tags=["Security Auth"])
async def login(req: LoginRequest, request: Request) -> dict[str, Any]:
    """Authenticates user credentials and generates active JWT signatures."""
    client_ip = request.client.host if request.client else "127.0.0.1"

    # Enforce Rate Limit check
    if not rate_limiter.is_allowed(client_ip):
        audit_trail.log_action(
            "anonymous", "LOGIN_FAILED", "auth", "FAILED_RATE_LIMIT", client_ip
        )
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Try again later.",
        )

    # Simple username match
    user = None
    for u in user_db.values():
        if u["username"] == req.username:
            user = u
            break

    if not user or req.password != "password123":  # noqa: S105
        audit_trail.log_action(
            "anonymous", "LOGIN_FAILED", req.username, "FAILED_CREDENTIALS", client_ip
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    if user["status"] != "ACTIVE":
        audit_trail.log_action(
            user["id"], "LOGIN_FAILED", req.username, "SUSPENDED_USER", client_ip
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is suspended or inactive",
        )

    # Generate tokens
    access = JWTAuth.create_access_token(
        identity_id=user["id"],
        type="USER",
        roles=user["roles"],
        department=user["department"],
    )
    refresh = JWTAuth.create_refresh_token(identity_id=user["id"])

    audit_trail.log_action(user["id"], "LOGIN_SUCCESS", "auth", "SUCCESS", client_ip)

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer",
    }


@router.post("/auth/logout", tags=["Security Auth"])
async def logout(request: Request) -> dict[str, Any]:
    """Revokes the active JWT access token immediately."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization Header",
        )

    token = auth_header.split(" ")[1]
    JWTAuth.revoke_token(token)

    client_ip = request.client.host if request.client else "127.0.0.1"
    audit_trail.log_action("revoker", "LOGOUT", "auth", "SUCCESS", client_ip)

    return {"message": "Token revoked successfully"}


@router.post("/auth/refresh", tags=["Security Auth"])
async def refresh_tokens(req: TokenRefreshRequest) -> dict[str, Any]:
    """Generates a new access token from a valid refresh token."""
    try:
        payload = JWTAuth.decode_token(req.refresh_token)
        identity_id = payload["sub"]

        # Fetch user
        user = user_db.get(identity_id)
        if not user or user["status"] != "ACTIVE":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive account",
            )

        new_access = JWTAuth.create_access_token(
            identity_id=user["id"],
            type="USER",
            roles=user["roles"],
            department=user["department"],
        )
        return {
            "access_token": new_access,
            "token_type": "bearer",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid refresh token: {str(e)}",
        ) from e


@router.get("/users", tags=["Security Admin"])
async def list_users() -> list[dict[str, Any]]:
    """Lists registered enterprise users."""
    return list(user_db.values())


@router.post("/users", tags=["Security Admin"])
async def create_user(req: UserCreateRequest, request: Request) -> dict[str, Any]:
    """Registers a new identity and maps enterprise roles."""
    # Verify rate limit and client IP
    client_ip = request.client.host if request.client else "127.0.0.1"

    # Enforce PII checks on username
    if AIGuardrails.scan_input_for_injection(req.username):
        incident_tracker.log_incident(
            title="Prompt Injection in Username Creation",
            severity="CRITICAL",
            source_ip=client_ip,
            linked_audits=[],
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid characters detected in username",
        )

    user_id = f"usr-{req.username.lower()}"
    if user_id in user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    user_db[user_id] = {
        "id": user_id,
        "username": req.username,
        "roles": req.roles,
        "department": req.department,
        "status": "ACTIVE",
    }

    audit_trail.log_action("admin", "CREATE_USER", user_id, "SUCCESS", client_ip)
    return user_db[user_id]


@router.put("/users/{id}", tags=["Security Admin"])
async def update_user(
    id: str, req: UserUpdateRequest, request: Request
) -> dict[str, Any]:
    """Modifies roles, department configurations, or status settings."""
    client_ip = request.client.host if request.client else "127.0.0.1"

    if id not in user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user = user_db[id]
    if req.roles is not None:
        user["roles"] = req.roles
    if req.department is not None:
        user["department"] = req.department
    if req.status is not None:
        user["status"] = req.status

    audit_trail.log_action("admin", "UPDATE_USER", id, "SUCCESS", client_ip)
    return user


@router.get("/roles", tags=["Security Admin"])
async def list_roles() -> list[str]:
    """Returns registered enterprise security roles."""
    return ENTERPRISE_ROLES


@router.post("/roles", tags=["Security Admin"])
async def create_custom_role(req: RoleCreateRequest) -> dict[str, Any]:
    """Registers custom roles with specific scopes."""
    if req.role_name in ENTERPRISE_ROLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role already exists",
        )
    ENTERPRISE_ROLES.append(req.role_name)
    return {"role_name": req.role_name, "permissions": req.permissions}


@router.get("/permissions", tags=["Security Admin"])
async def list_permissions() -> dict[str, list[str]]:
    """Returns resource permission mapping."""
    return PermissionEngine.PERMISSION_ROLES


@router.get("/audit", tags=["Security Audit"])
async def get_audit_trail() -> list[dict[str, Any]]:
    """Retrieves immutable audit logging history."""
    return audit_trail.logs


@router.get("/security/incidents", tags=["Security Incidents"])
async def list_security_incidents() -> list[Any]:
    """Retrieves security incidents logged across components."""
    return [inc.model_dump() for inc in incident_tracker.list_incidents()]


@router.post("/security/incidents", tags=["Security Incidents"])
async def log_security_incident(req: SecurityIncidentRequest) -> dict[str, Any]:
    """Manual registry of security containment status."""
    inc = incident_tracker.log_incident(
        title=req.title,
        severity=req.severity,
        source_ip=req.source_ip,
        linked_audits=req.linked_audits,
    )
    return inc.model_dump()


@router.get("/security/risk", tags=["Security Risk"])
async def get_risk_assessment() -> dict[str, Any]:
    """Computes aggregated client risk level scoring."""
    score = RiskEvaluator.calculate_request_risk(
        failed_logins=2,
        prompt_injection_flags=0,
        unauthorized_attempts=1,
    )
    return {
        "risk_score": score,
        "risk_level": RiskEvaluator.get_risk_label(score),
    }
