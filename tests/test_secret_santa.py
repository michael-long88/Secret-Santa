import json

import pytest

from src.constants import PARTICIPANTS_TEST_FILE, TEST_DATA_DIR
from src.secret_santa import SecretSanta


@pytest.fixture(scope="module", autouse=True)
def cleanup_test_files():
    """Clean up any test files created during testing."""
    yield

    if TEST_DATA_DIR.exists():
        for file in TEST_DATA_DIR.glob("*.json"):
            file.unlink()

        TEST_DATA_DIR.rmdir()


@pytest.fixture
def secret_santa():
    """Create a SecretSanta instance in test mode."""
    return SecretSanta(test_mode=True)


def test_secret_santa_creates_valid_pairings(secret_santa: SecretSanta):
    """Test that Secret Santa algorithm creates valid pairings."""
    secret_santa.create_pairings()
    pairings = secret_santa.pairings

    # Test that pairings were created
    assert pairings, "No pairings were created"

    # Test that each person gives exactly one gift
    assert len(pairings) == len(secret_santa.participants), (
        "Not everyone is giving a gift"
    )

    # Test that each person receives exactly one gift
    receivers = set(pairings.values())
    assert len(receivers) == len(secret_santa.participants), (
        "Not everyone is receiving a gift"
    )

    # Test that no invalid matches exist
    for gifter, giftee in pairings.items():
        person = next(
            person for person in secret_santa.participants if person.name == gifter
        )
        assert giftee not in person.invalid_matches, (
            f"Invalid match: {gifter} -> {giftee}"
        )

    print_pairings(pairings)
    assert False


def test_secret_santa_handles_impossible_constraints():
    """Test that Secret Santa algorithm properly handles impossible constraints."""
    with open(PARTICIPANTS_TEST_FILE, "r") as f:
        data: dict = json.load(f)

    TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)
    impossible_file = TEST_DATA_DIR / "impossible_participants.json"

    # Modify the data to create an impossible constraint set
    # Make the first person have everyone as invalid matches
    all_names = list(data.keys())
    data[all_names[0]]["invalid_matches"] = all_names

    with open(impossible_file, "w") as f:
        json.dump(data, f, indent=2)

    impossible_santa = SecretSanta(test_mode=True)
    impossible_santa.paticipants_file = impossible_file
    impossible_santa.participants = impossible_santa.get_participants()

    with pytest.raises(ValueError):
        impossible_santa.create_pairings()


def test_repeated_runs_produce_different_pairings(secret_santa: SecretSanta):
    """Test that multiple runs produce different pairings due to randomization."""
    secret_santa.create_pairings()
    first_pairings = secret_santa.pairings.copy()

    different_found = False

    for _ in range(5):
        secret_santa.pairings = {}
        secret_santa.create_pairings()

        # Check if pairings are different
        if any(
            first_pairings[gifter] != secret_santa.pairings[gifter]
            for gifter in first_pairings
        ):
            different_found = True
            break

    # It's possible but unlikely that we get the same pairings multiple times
    # so we use a soft assertion
    assert different_found, "Expected different pairings across multiple runs"


def print_pairings(pairings: dict[str, str]):
    """Helper function to print pairings for debugging."""
    for gifter, giftee in sorted(pairings.items()):
        print(f"{gifter} → {giftee}")
