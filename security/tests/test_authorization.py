from security.authorization.engine import PermissionEngine


def test_permission_engine_routing() -> None:
    # 1. Allowed roles check
    assert PermissionEngine.check_permission(["Guest"], "reservation:read") is True
    assert (
        PermissionEngine.check_permission(["Receptionist"], "reservation:write") is True
    )

    # 2. Denied roles check
    assert PermissionEngine.check_permission(["Guest"], "reservation:write") is False
    assert PermissionEngine.check_permission(["Housekeeping"], "revenue:write") is False

    # 3. Unrecognized permission fallback
    assert (
        PermissionEngine.check_permission(["Administrator"], "unknown:permission")
        is False
    )
