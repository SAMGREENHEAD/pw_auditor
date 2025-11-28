# pw-auditor  
Offline Password Strength Auditor — Entropy + Pattern Analysis

`pw-auditor` is a lightweight, privacy-preserving Python tool for evaluating password strength entirely offline.  
It combines entropy estimation with pattern detection to identify weak or predictable passwords and provide actionable suggestions.

No network calls. No APIs. No data leaves your machine.

---

## Features

### Offline Entropy Analysis  
Calculates Shannon-style entropy based on character class usage:
- lowercase  
- uppercase  
- digits  
- symbols  

### Pattern Detection  
Identifies weak and predictable password structures, including:
- Years and dates (e.g., 1999, 2024)
- Repeated characters (aaaaaa)
- Repeated sequences (abcabc, 123123)
- Keyboard patterns (qwerty, asdf, 1qaz)
- Dictionary word matches (via included wordlist)
- Common password list matches

### Security Rating  
Each password receives a score:
- Very Weak  
- Weak  
- Moderate  
- Strong  
- Very Strong  

### Actionable Suggestions  
Outputs improvement recommendations based on detected weaknesses.

### Command-Line Interface  
Supports auditing:
- A single password  
- A file containing multiple passwords  
- Standard input (pipe mode)

---

## Installation (Local Development)

Clone the repository:

```bash
git clone https://github.com/SAMGREENHEAD/pw_auditor.git
cd pw_auditor
```

Install in editable mode:

```bash
pip install -e .
```

This makes the `pw-auditor` CLI tool available globally.

---

## Usage

### Audit a single password
```bash
pw-auditor "P@ssw0rd123"
```

### Audit a file of passwords
```bash
pw-auditor -f passwords.txt
```

### Pipe input
```bash
echo "hello123" | pw-auditor
```

### Example Output
```json
{
  "password": "P@ssw0rd123",
  "entropy_bits": 57.3,
  "patterns": ["contains_year"],
  "score": "Moderate",
  "suggestions": [
    "Password length and character variety look reasonable.",
    "Avoid using years or dates in passwords."
  ]
}
```

---

## Using as a Python Library

```python
from pw_auditor import audit

result = audit("StrongPass!123")
print(result)
```

---

## Running Tests

Install pytest:

```bash
pip install pytest
```

Run test suite:

```bash
pytest
```

With coverage:

```bash
pytest --cov=pw_auditor
```


---

## Security Notes
- All processing happens locally.
- Passwords are not transmitted, collected, or stored.
- Avoid saving sensitive passwords to files when possible.

---

## Contributing  
Contributions are welcome.  
To suggest improvements or new pattern checks, please open an issue or submit a pull request.

---

## License  
MIT License.

---

## Repository  
https://github.com/SAMGREENHEAD/pw_auditor
