from pw_auditor.patterns import detect_patterns

def test_detect_year():
    assert "contains_year" in detect_patterns("Hello1999")

def test_repeated_chars():
    assert "repeated_chars" in detect_patterns("aaaaaa")

def test_keyboard_pattern():
    flags = detect_patterns("myqwertypass")
    assert any("keyboard_pattern" in f for f in flags)
