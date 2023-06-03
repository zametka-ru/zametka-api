from fastapi_jwt_auth import AuthJWT

from adapters.repository import AuthRepository

from core.db import User


async def get_current_user(Authorize: AuthJWT, auth_repository: AuthRepository) -> User:
    user_email = Authorize.get_jwt_subject()

    user = await auth_repository.get_user_by_email(user_email)

    return user
