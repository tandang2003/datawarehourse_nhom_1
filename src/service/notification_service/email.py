from enum import Enum

from fastapi_mail import MessageSchema, FastMail
import asyncio
from src.config.mail import email_config
from src.config.setting import MAIL_TO


class EmailCategory(Enum):
    INFO = "info"
    ALERT = "alert"
    ERROR = "error"


async def sent_mail(message: str, type: EmailCategory):
    subject = ""
    match type:
        case EmailCategory.INFO:
            subject = "Info"
        case EmailCategory.ALERT:
            subject = "Alert"
        case EmailCategory.ERROR:
            subject = "Error"
        case _:
            subject = "Unknown"
    message = MessageSchema(
        subject=subject,
        body=message,
        recipients=MAIL_TO,
        subtype="plain"
    )
    fm = FastMail(email_config)
    try:
        await fm.send_message(message)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    asyncio.run(sent_mail("Hello, World!", EmailCategory.INFO))
