from uuid import UUID

from pydantic import BaseModel


class UserSchema(BaseModel):
    first_name: str
    last_name: str


class IdentitySchema(BaseModel):
    identity_id: UUID
