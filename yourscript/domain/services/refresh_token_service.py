from domain.entities import RefreshToken

from domain.value_objects.user_id import UserId


class RefreshTokenService:
    def create(self, token: str, user_id: UserId) -> RefreshToken:
        return RefreshToken(
            token=token,
            user_id=user_id,
        )
