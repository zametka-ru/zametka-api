import jwt


class JWTCheckError(jwt.exceptions.DecodeError):
    """Base JWT check error"""


class JWTExpiredError(JWTCheckError):
    """Raises when jwt exceeded expires time"""

    def __init__(self, message="Token is expired.", *args):
        self.message = message

        super().__init__(self, message, *args)


class JWTAlreadyUsedError(JWTCheckError):
    """Raises when user uses jwt second time"""

    def __init__(self, message="Token already used", *args):
        self.message = message

        super().__init__(self, message, *args)
