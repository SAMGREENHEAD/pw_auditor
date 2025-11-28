from pw_auditor.entropy import calculate_entropy

def test_entropy_empty():
    assert calculate_entropy("") == 0

def test_entropy_increases_with_length():
    short = calculate_entropy("abc")
    long = calculate_entropy("abcdefgh")
    assert long > short

def test_entropy_mixed_charsets():
    lower = calculate_entropy("abcdef")
    mixed = calculate_entropy("Abc123!")
    assert mixed > lower
