import json
import ssl
from datetime import datetime

import polars as pl
import yaml

from src.config import Config
from src.constants import HISTORY_FILE, PARTICIPANTS_FILE


def get_participants() -> dict[str, dict[str, str]]:
    """
    Load and return the participants data from the participants.json file.

    Returns
    -------
    dict[str, dict[str, str]]
        The loaded participants data.
    """
    participants = {}

    with open(PARTICIPANTS_FILE) as json_file:
        total_partipants = json.load(json_file)
        participants = {
            participant_name: {
                "email": total_partipants[participant_name]["email"],
                "match": total_partipants[participant_name]["invalid_matches"][-1],
            }
            for participant_name in total_partipants
        }

    return participants


def get_config() -> Config:
    """
    Load and return the configuration settings from the email_config.yaml file.

    Returns
    -------
    Config
        The loaded configuration settings.
    """
    email_config = yaml.safe_load(open("email_config.yaml"))

    return Config(
        email_config["PORT"],
        email_config["USERNAME"],
        email_config["PASSWORD"],
        email_config["SENDER_EMAIL"],
        email_config["SMTP_SERVER"],
        ssl.create_default_context(),
    )


def get_historical_matches(gifter_name: str, year: int | None):
    """
    Load and print the historical match for the given gifter from the pairings.csv file.

    Parameters
    ----------
    gifter_name : str
        The name of the gifter whose match we want to retrieve.
    year : int | None
        The year for which we want to retrieve the match.
        If None, retrieve all matches besides the current one.
    """
    pairings = pl.read_csv(HISTORY_FILE)
    if year is None:
        matches = pairings.filter(
            pl.col("gifter").eq(gifter_name),
            pl.col("year") < datetime.now().year,
        )
    else:
        matches = pairings.filter(
            pl.col("gifter").eq(gifter_name),
            pl.col("year").eq(year),
        )
    print(matches)
