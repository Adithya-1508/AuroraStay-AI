from datetime import time

from security.abac.policy import ABACPolicyEngine
from security.rbac.roles import RBACManager


def test_rbac_permissions_consolidation() -> None:
    # 1. Standard single role
    perms = RBACManager.get_permissions_for_roles(["Guest"])
    assert "reservation:read" in perms
    assert len(perms) == 1

    # 2. Combined roles
    perms_combined = RBACManager.get_permissions_for_roles(["Guest", "Housekeeping"])
    assert "reservation:read" in perms_combined
    assert "housekeeping:read" in perms_combined
    assert len(perms_combined) == 3


def test_abac_context_evaluation() -> None:
    # 1. IP Blacklist check
    assert (
        ABACPolicyEngine.evaluate_context("192.168.1.99", "Reception", "Reception")
        is False
    )
    assert (
        ABACPolicyEngine.evaluate_context("127.0.0.1", "Reception", "Reception") is True
    )

    # 2. Shift time check (during operational window)
    time_day = time(12, 0)
    assert (
        ABACPolicyEngine.evaluate_context(
            "127.0.0.1", "Reception", "Reception", time_day
        )
        is True
    )

    # 3. Shift time check (outside operational window)
    time_night = time(2, 0)
    assert (
        ABACPolicyEngine.evaluate_context(
            "127.0.0.1", "Reception", "Reception", time_night
        )
        is False
    )

    # 4. Shift time check overrides (managers allowed)
    assert (
        ABACPolicyEngine.evaluate_context(
            "127.0.0.1", "Administration", "Reception", time_night
        )
        is True
    )

    # 5. Department isolation (unrelated department access denied)
    assert (
        ABACPolicyEngine.evaluate_context(
            "127.0.0.1", "Housekeeping", "Revenue", time_day
        )
        is False
    )
    # Allowed when departments match
    assert (
        ABACPolicyEngine.evaluate_context(
            "127.0.0.1", "Housekeeping", "Housekeeping", time_day
        )
        is True
    )
    # Allowed when department is ALL or Administration
    assert (
        ABACPolicyEngine.evaluate_context(
            "127.0.0.1", "Administration", "Revenue", time_day
        )
        is True
    )
