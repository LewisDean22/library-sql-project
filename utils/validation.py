import re


def validate_email(email: str) -> None:
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    if not re.fullmatch(pattern, email):
        raise ValueError(f"Invalid email address: {email}")
