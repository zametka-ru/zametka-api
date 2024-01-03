from fastapi_mail import FastMail, MessageSchema, MessageType
from jinja2 import Environment
from starlette.background import BackgroundTasks

from zametka.access_service.application.common.token_sender import MailTokenSender
from zametka.access_service.domain.value_objects.email_token import EmailToken
from zametka.access_service.domain.value_objects.user_email import UserEmail


def get_message_schema(subject: str, to_email: UserEmail, html: str) -> MessageSchema:
    message_schema = MessageSchema(
        subject=subject,
        recipients=[to_email.to_raw()],
        body=html,
        subtype=MessageType.html,
    )

    return message_schema


class MailTokenSenderImpl(MailTokenSender):
    """MailTokenSenderInterface implementation"""

    mail: FastMail
    background_tasks: BackgroundTasks
    token_link: str

    def __init__(
        self,
        mail: FastMail,
        background_tasks: BackgroundTasks,
        jinja: Environment,
        token_link: str,
    ) -> None:
        self._mail = mail
        self._background_tasks = background_tasks
        self._jinja = jinja
        self._token_link = token_link

    def _render_html(self, token: EmailToken) -> str:
        template = self._jinja.get_template("confirmation-mail.html")

        rendered: str = template.render(
            token_link=self._token_link.format(token.to_raw())
        )

        return rendered

    def send(self, token: EmailToken, subject: str, to_email: UserEmail) -> None:
        """Send email token to the user"""

        html = self._render_html(token)

        self._background_tasks.add_task(
            self._mail.send_message,
            get_message_schema(subject=subject, html=html, to_email=to_email),
            template_name="confirmation-mail",
        )
