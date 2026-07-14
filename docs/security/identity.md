# Identity & Directory Services

This module governs the representation of human users, system agents, and programmatic service profiles.

## Identity Entity Model Schema

```python
class Identity(BaseModel):
    identity_id: str
    type: IdentityType  # USER, AGENT, SERVICE
    name: str
    owner: Optional[str] = None
    status: IdentityStatus  # ACTIVE, SUSPENDED, DELETED
    assigned_roles: List[str] = []
    department: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

## Directory Administration Guidelines

- **User Registration**: Every human identity must belong to exactly one department (e.g., `Revenue`, `Reception`, `Housekeeping`) and have a set of assigned enterprise roles.
- **Agent Provisioning**: Autonomously acting AI models must be registered as `IdentityType.AGENT` with designated human owners accountable for their requests.
- **Identity Suspension**: Suspend identities immediately by setting status to `IdentityStatus.SUSPENDED`, which revokes all active sessions on downstream components.
