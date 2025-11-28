from pw_auditor.auditor import audit

def test_audit_returns_dict():
    res = audit("Test123!")
    assert isinstance(res, dict)

def test_audit_has_entropy():
    res = audit("Test123!")
    assert "entropy_bits" in res

def test_weak_password_flagged():
    res = audit("password")
    assert res["score"] in ["Weak", "Very Weak"]
