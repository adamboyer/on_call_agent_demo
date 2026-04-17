from app.services.approval_service import ApprovalService


def test_only_allowed_user_can_approve():
    service = ApprovalService()
    service.create_approval("inc-1", "U_ALLOWED", "restart")

    assert service.is_allowed("inc-1", "U_ALLOWED", "restart") is True
    assert service.is_allowed("inc-1", "U_OTHER", "restart") is False
