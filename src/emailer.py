import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from rich.logging import RichHandler

from src.config import Config

logging.basicConfig(
    level="INFO", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)


def send_email_to(participants: dict[str, dict[str, str]], config: Config) -> None:
    with smtplib.SMTP_SSL(
        config.smtp_server, config.port, context=config.ssl_context
    ) as server:
        server.login(config.username, config.password)

        for participant_name, participant_info in participants.items():
            email = participant_info["email"]
            match = participant_info["match"]

            message = MIMEMultipart()
            message["From"] = config.sender_email
            message["To"] = email
            message["Subject"] = f"Secret Santa drawing for {participant_name}"
            body = f"Hello, {participant_name}. \n\nYou have drawn {match} for this year's Secret Santa."
            message.attach(MIMEText(body, "plain"))

            logging.info(f"Sending email to {participant_name}...")
            server.sendmail(config.sender_email, email, message.as_string())
