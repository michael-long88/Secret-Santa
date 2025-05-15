# Secret-Santa

A Python application to assign and email Secret Santa participants. The application reads participant information from a JSON file, creates optimal pairings, and sends emails to participants with their assigned Secret Santa.

## Overview

The script assigns a recipient to each participant based on an exclusion list in the `participants.json` file (rename the template file in the data directory to `participants.json`). The application uses a compatibility graph and optimal matching algorithm to ensure everyone gets a valid Secret Santa. If a valid pairing cannot be found, the process will retry.

After the pairings have been completed, the program will email each participant with the name of their Secret Santa. Pairings are written to a CSV file with the year, gifter, and giftee information for historical tracking.

## Requirements

- Python 3.13+
- Dependencies listed in pyproject.toml

## Project Structure

- `main.py`: Entry point with Typer CLI commands
- `src/`: Core application code
  - `secret_santa.py`: Contains the Secret Santa matching algorithm
  - `emailer.py`: Handles sending emails to participants
  - `config.py`: Application configuration
  - `constants.py`: Project constants and file paths
  - `utils.py`: Utility functions
- `data/`: Data files
  - `participants.json`: Participant information
  - `pairings.csv`: Historical pairings data

## Getting Started

1. Create a `participants.json` file in the data directory by copying and renaming the template.
    - You don't need to make a copy, but the tests will fail if you don't.
1. Copy and rename `email_config_template.yaml` to `email_config.yaml`.
1. Configure your email settings in `email_config.yaml`.
1. Run the application using the CLI commands.

## Usage

The application provides several commands through a Typer CLI interface:

```bash
# Generate Secret Santa pairings and send emails
python main.py generate-list

# Send emails to participants (all or specific recipient)
python main.py email [--recipient "Name"]

# View historical matches for a participant
python main.py history "Name" [--year YEAR]
```

## Development

### Setting Up the Development Environment

This project uses [uv](https://docs.astral.sh/uv/) for dependency management, which is a fast Python package installer and resolver.

#### Installing uv

To install uv, follow the instructions on their [install page](https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_1).

#### Managing Dependencies

When getting start for the first time, run `uv sync` from the project root.

To activate the environment:

```bash
# Activate the virtual environment
source .venv/bin/activate  # On Linux/macOS
source .venv\Scripts\activate     # On Windows
```

To add a new dependency:

```bash
uv add package-name
```

To remove a dependency:

```bash
uv remove package-name
```

### Running Tests

To run tests, simply run `pytest` from the project root.

### Linting and formatting

If you're using VSCode, I recommend installing the Ruff extension and adding this to `.vscode/settings.json` in the project root. It will automatically format the code when you save.

```json
{
    "[python]": {
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.fixAll": "explicit",
            "source.organizeImports": "explicit"
        },
        "editor.defaultFormatter": "charliermarsh.ruff"
    }
}
```

To manually run ruff:

```bash
uv run ruff check .
uv run ruff check . --select I
uv run ruff format .
```

## Notes

The email functionality allows you to resend Secret Santa assignments to participants who may have deleted their emails. This is also useful when email provider security settings change and you don't want to reassign all matches.
