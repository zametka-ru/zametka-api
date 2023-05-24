from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/hello/")
async def hello(session: Session = Depends()) -> str:
    return "hello"
