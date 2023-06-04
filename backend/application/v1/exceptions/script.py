class IsNotExists(Exception):
    """Raises when object with given arguments is not exists"""

    def __init__(
        self, object_type: type, message: str = "{} object is not exists", *args
    ):
        self._object_type = object_type

        self.message = message.format(self.get_normalized_type_name())

        super().__init__(self, message, *args)

    def get_normalized_type_name(self) -> str:
        """Get a qualname from a object type"""

        return self._object_type.__qualname__


class RestrictScriptAccess(Exception):
    """Raises when access to script was restricted"""

    def __init__(self, message: str, *args):
        self.message = message

        super().__init__(self, message, *args)
