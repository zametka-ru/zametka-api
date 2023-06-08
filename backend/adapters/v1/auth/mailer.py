from fastapi_mail import FastMail, MessageSchema, MessageType

from starlette.background import BackgroundTasks

from application.v1.auth.interfaces import TokenSenderInterface


class Mailer(TokenSenderInterface):
    mail: FastMail
    background_tasks: BackgroundTasks

    def __init__(self, mail: FastMail, background_tasks: BackgroundTasks) -> None:
        self._mail = mail
        self._background_tasks = background_tasks

    def _get_message_schema(
        self, subject: str, to_email: str, html: str
    ) -> MessageSchema:
        message_schema = MessageSchema(
            subject=subject,
            recipients=[to_email],
            body=html,
            subtype=MessageType.html,
        )

        return message_schema

    def send(self, to_email: str, subject: str, html: str) -> None:
        """Send email token to the user"""

        self._background_tasks.add_task(
            self._mail.send_message,
            self._get_message_schema(subject=subject, html=html, to_email=to_email),
        )
