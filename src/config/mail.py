from fastapi_mail import ConnectionConfig
from src.config.setting import MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM, MAIL_SERVER, MAIL_FROM_NAME

email_config = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,  # Must be a string
    MAIL_PASSWORD=MAIL_PASSWORD,  # Must be a string
    MAIL_FROM=MAIL_FROM,  # Must be a valid email address as a string
    MAIL_PORT=587,  # Must be an integer
    MAIL_SERVER=MAIL_SERVER,  # Must be a string
    MAIL_FROM_NAME=MAIL_FROM_NAME,  # Must be a string
    MAIL_STARTTLS=True,  # StartTLS instead of MAIL_TLS
    MAIL_SSL_TLS=False,  # SSL/TLS instead of MAIL_SSL
    USE_CREDENTIALS=True,  # Use credentials
    VALIDATE_CERTS=True
)
