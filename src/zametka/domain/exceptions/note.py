from .base import DomainError


class NoteDataError(DomainError):
    pass


class NoteNotExistsError(DomainError):
    pass


class NoteAccessDeniedError(DomainError):
    pass


class InvalidNoteTextError(NoteDataError):
    pass


class InvalidNoteTitleError(NoteDataError):
    pass
