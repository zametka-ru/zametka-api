"""Services (queries) for the User model"""

from sqlalchemy.orm import Session
from sqlalchemy import select

from core.db.models.users import User


async def create_user(
    session: Session,
    user: dict,
) -> User:
    """
    Register user
    """

    user_obj = User(
        email=user.get("email"),
        password=user.get("password"),
        first_name=user.get("first_name"),
        last_name=user.get("last_name"),
        joined_at=user.get("joined_at"),
        is_superuser=user.get("is_superuser"),
        is_active=user.get("is_active"),
    )

    session.add(user_obj)

    return user_obj


async def get_user_by_email(session: Session, user_email: str) -> User:
    """Get user by email"""

    q = select(User).where(User.email == user_email)

    res = await session.execute(q)
    user: User = res.scalar()

    return user


async def get_user_by_id(session: Session, user_id: int) -> User:
    """Get user by id"""

    q = select(User).where(User.id == user_id)

    res = await session.execute(q)
    user: User = res.scalar()

    return user


async def make_user_active(user: User):
    """
    Set user.is_active to True
    """

    user.is_active = True
