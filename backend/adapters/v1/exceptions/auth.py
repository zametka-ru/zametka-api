import jwt


class JWTExpiredError(jwt.exceptions.DecodeError):
    """Raises when jwt exceeded expires time"""

    def __init__(self, message="Token is expired.", *args):
        self.message = message

        super().__init__(self, message, *args)


class JWTAlreadyUsedError(jwt.exceptions.DecodeError):
    """Raises when user uses jwt second time"""

    def __init__(self, message="Token already used", *args):
        self.message = message

        super().__init__(self, message, *args)
