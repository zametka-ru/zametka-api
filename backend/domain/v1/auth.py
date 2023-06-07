def validate_password(password: str) -> None:
    """Validate password (business logic), may raise ValueError"""

    error_messages = {
        "Password must contain an uppercase letter.": lambda s: any(
            x.isupper() for x in s
        ),
        "Password must contain a lowercase letter.": lambda s: any(
            x.islower() for x in s
        ),
        "Password must contain a digit.": lambda s: any(x.isdigit() for x in s),
        "Password cannot contain white spaces.": lambda s: not any(
            x.isspace() for x in s
        ),
    }

    for message, password_validator in error_messages.items():
        if not password_validator(password):
            raise ValueError(message)
