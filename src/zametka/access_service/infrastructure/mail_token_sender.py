from fastapi_mail import FastMail, MessageSchema, MessageType
from jinja2 import Environment
from starlette.background import BackgroundTasks

from zametka.access_service.application.common.token_sender import TokenSender
from zametka.access_service.domain.entities.confirmation_token import (
    IdentityConfirmationToken,
)
from zametka.access_service.domain.entities.user_identity import UserIdentity
from zametka.access_service.domain.value_objects.user_email import UserEmail


def get_message_schema(subject: str, to_email: UserEmail, html: str) -> MessageSchema:
    message_schema = MessageSchema(
        subject=subject,
        recipients=[to_email.to_raw()],
        body=html,
        subtype=MessageType.html,
    )

    return message_schema


class MailTokenSenderImpl(TokenSender):
    """TokenSender email implementation"""

    mail: FastMail
    background_tasks: BackgroundTasks
    token_link: str

    def __init__(
        self,
        mail: FastMail,
        jinja: Environment,
        token_link: str,
    ) -> None:
        self._mail = mail
        self._jinja = jinja
        self._token_link = token_link

    def _render_html(self, confirmation_token: IdentityConfirmationToken) -> str:
        template = self._jinja.get_template("confirmation-mail.html")

        rendered: str = template.render(
            token_link=self._token_link.format(confirmation_token.token.to_raw())
        )

        return rendered

    async def send(self, token: IdentityConfirmationToken, user: UserIdentity) -> None:
        """Send email token to the user"""

        html = self._render_html(token)
        message = get_message_schema(
            "ЗАВЕРШИТЕ РЕГИСТРАЦИЮ В zametka.",
            html=html,
            to_email=user.email,
        )

        await self.mail.send_message(message, "confirmation-mail")
