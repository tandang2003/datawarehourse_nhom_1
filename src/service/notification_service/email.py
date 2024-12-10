import asyncio
from enum import Enum

from fastapi_mail import MessageSchema, FastMail

from src.config.mail import email_config
from src.config.setting import MAIL_TO


class LABEL(Enum):
    INFO = "INFO"
    ALERT = "ALERT"
    ERROR = "ERROR"


class EmailTemplate:
    def __init__(self, subject: str,
                 status: str,
                 code: int,
                 message: str,
                 file_log: str = None,
                 subtype: str = 'html',
                 recipients: list = MAIL_TO,
                 label: LABEL = LABEL.INFO):
        self.subject = subject
        self.subtype = subtype
        self.recipients = recipients
        self._status = status
        self._code = code
        self._message = message
        self._file_log = file_log
        self._label = label

    def to_message_schema(self) -> MessageSchema:
        return MessageSchema(
            subject=f"""[{self._label.name}]{self.subject}""",
            body=f"""
                <p><b>Status:</b> {self._status}</p>
                <p><b>Code:</b> {self._code}</p>
                <p><b>Message:</b> {self._message}</p>   
                {self._file_log and f'<p><b>File log:</b> {self._file_log}</p>'}
                """,
            recipients=self.recipients,
            subtype=self.subtype
        )

    def sent_mail(self):
        asyncio.run(self._sent_mail_async())

    async def _sent_mail_async(self):
        fm = FastMail(email_config)
        try:
            await fm.send_message(self.to_message_schema())
        except Exception as e:
            print(f"Error: {e}")


if __name__ == '__main__':
    from src.service.AppException import STATUS

    email_template = EmailTemplate(subject="Test",
                                   status=STATUS.FILE_ERROR.name,
                                   code=STATUS.FILE_ERROR.value,
                                   message="This is a test email",
                                   file_log="test.log",
                                   label=LABEL.ERROR)
    asyncio.run(email_template.sent_mail())
