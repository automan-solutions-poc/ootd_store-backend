import smtplib
from email.message import EmailMessage
import ssl
from app.core.config import settings
from app.core.logging import logger

class EmailService:
    @staticmethod
    def send_email(to_email: str, subject: str, content: str):
        if not all([settings.SMTP_HOST, settings.SMTP_USER, settings.SMTP_PASSWORD]):
            logger.warning("email_skip", reason="SMTP settings not configured")
            return

        msg = EmailMessage()
        msg.set_content(content)
        msg["Subject"] = subject
        msg["From"] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
        msg["To"] = to_email

        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls(context=context)
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
            logger.info("email_sent", to=to_email, subject=subject)
        except Exception as e:
            logger.error("email_error", error=str(e), to=to_email)

    @staticmethod
    async def send_order_confirmation(email: str, order_id: str):
        EmailService.send_email(
            email,
            "Order Confirmed",
            f"Your order {order_id} has been confirmed."
        )

    @staticmethod
    async def send_order_failure(email: str, order_id: str):
        EmailService.send_email(
            email,
            "Order Failed",
            f"Your order {order_id} has failed to process with our provider."
        )

    @staticmethod
    async def send_password_reset(email: str):
        EmailService.send_email(
            email,
            "Password Reset",
            "Your password has been successfully reset."
        )
