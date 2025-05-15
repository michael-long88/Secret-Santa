import logging
from typing import Optional

import typer
from rich.logging import RichHandler
from typing_extensions import Annotated

from src.emailer import send_email_to
from src.secret_santa import SecretSanta
from src.utils import get_config, get_historical_matches, get_participants

logging.basicConfig(
    level="INFO", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)

app = typer.Typer()


@app.command("generate-list")
def generate_list():
    """
    Generate a Secret Santa list.
    """
    logging.info("Generating Secret Santa list...")
    config = get_config()

    secret_santa = SecretSanta(test_mode=False)
    secret_santa.create_pairings()
    secret_santa.add_new_pairings()
    secret_santa.update_invalid_matches()

    recipients = get_participants()
    send_email_to(recipients, config)


@app.command("email")
def send_emails(
    recipient: Annotated[
        str,
        typer.Option(
            help="First and last name of the person to send an email to. If no name is provided, all participants will be sent emails."
        ),
    ] = None,
):
    """
    Send emails to all participants.
    """
    logging.info("Sending emails to participants...")
    config = get_config()

    recipients = get_participants()
    if recipient is not None:
        try:
            recipients = {recipient: recipients[recipient]}
        except KeyError:
            logging.error(f"No participant found with the name '{recipient}'.")
            return

    send_email_to(recipients, config)


@app.command("history")
def get_history(
    recipient: Annotated[
        str,
        typer.Argument(help="First and last name of the person to send an email to."),
    ],
    year: Annotated[
        Optional[int],
        typer.Option(help="First and last name of the person to send an email to."),
    ] = None,
):
    get_historical_matches(recipient, year)


if __name__ == "__main__":
    app()
