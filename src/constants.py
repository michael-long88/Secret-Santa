from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
TEST_DIR = PROJECT_ROOT / "tests"
TEST_DATA_DIR = TEST_DIR / "data"

HISTORY_FILE = DATA_DIR / "pairings.csv"
PARTICIPANTS_FILE = DATA_DIR / "participants.json"
PARTICIPANTS_TEST_FILE = DATA_DIR / "participants_template.json"
