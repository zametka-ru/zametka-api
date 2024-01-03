from fastapi import APIRouter, BackgroundTasks, Depends, Request, Response
from fastapi_another_jwt_auth import AuthJWT

from zametka.access_service.application.common.id_provider import IdProvider
from zametka.access_service.application.dto import UserIdentityDTO
from zametka.access_service.application.verify_email import TokenInputDTO
from zametka.access_service.application.authorize import AuthorizeInputDTO
from zametka.access_service.application.create_identity import IdentityInputDTO

from zametka.access_service.presentation.interactor_factory import InteractorFactory
from zametka.access_service.presentation.web_api.schemas.user import (
    AuthorizeSchema,
    CreateIdentitySchema,
)

router = APIRouter(
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def create_identity(
    data: CreateIdentitySchema,
    background_tasks: BackgroundTasks,
    ioc: InteractorFactory = Depends(),
) -> UserIdentityDTO:
    async with ioc.create_identity(background_tasks=background_tasks) as interactor:
        response = await interactor(
            IdentityInputDTO(
                email=data.email,
                password=data.password,
                additional_info=data.additional_info,
            )
        )

        return response


@router.post("/authorize")
async def authorize(
    data: AuthorizeSchema,
    token_processor: AuthJWT = Depends(),
    ioc: InteractorFactory = Depends(),
) -> UserIdentityDTO:
    async with ioc.authorize() as interactor:
        response = await interactor(
            AuthorizeInputDTO(
                email=data.email,
                password=data.password,
            )
        )

    subject = response.identity_id
    access = token_processor.create_access_token(subject=str(subject))
    token_processor.set_access_cookies(access)

    return response


@router.get("/me")
async def get_identity(
    id_provider: IdProvider = Depends(),
    ioc: InteractorFactory = Depends(),
) -> UserIdentityDTO:
    async with ioc.get_identity(id_provider=id_provider) as interactor:
        response = await interactor()

    return response


@router.get(
    "/ensure-can-edit"
)  # TODO: move AuthJWT to trash and write JWTTokenProcessor for this
async def ensure_can_edit(
    request: Request,
    _id_provider: IdProvider = Depends(),
) -> Response:
    """Ensure that requester can do modify(POST, PUT, PATCH, DELETE) requests"""

    request.scope["method"] = next(iter(AuthJWT._csrf_methods))  # noqa
    jwt_auth = AuthJWT(request)

    jwt_auth._verify_and_get_jwt_in_cookies("access", request)  # noqa

    return Response(status_code=200)


@router.get("/verify/{token}")
async def verify_email(token: str, ioc: InteractorFactory = Depends()) -> None:
    async with ioc.verify_email() as interactor:
        await interactor(
            TokenInputDTO(
                token=token,
            )
        )
