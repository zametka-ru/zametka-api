from domain.v1.entities.refresh_token import RefreshToken

from domain.v1.value_objects.user_id import UserId


class RefreshTokenService:
    def create(self, token: str, user_id: UserId) -> RefreshToken:
        return RefreshToken(
            token=token,
            user_id=user_id,
        )
