import json
import random
from datetime import datetime

import polars as pl

from src.constants import HISTORY_FILE, PARTICIPANTS_FILE, PARTICIPANTS_TEST_FILE


class Person:
    def __init__(self, name: str, email: str, invalid_match: list[str]):
        self.name: str = name
        self.email: str = email
        self.invalid_matches: list[str] = invalid_match

    def __str__(self):
        return f"{self.name}, {self.email}"


class SecretSanta:
    def __init__(self, test_mode: bool):
        self.pairings: dict[str, str] = {}
        self.participants_dict: dict[str, dict[str, str | list[str]]] = {}
        self.test_mode: bool = test_mode
        self.paticipants_file = (
            PARTICIPANTS_TEST_FILE if test_mode else PARTICIPANTS_FILE
        )
        self.participants: list[Person] = self.get_participants()

    def get_participants(self) -> list[Person]:
        """
        Load and return the participants data from the participants.json file.

        Returns
        -------
        list[Person]
            The loaded participants data.
        """
        participants = []
        with open(self.paticipants_file) as json_file:
            participants_json = json.load(json_file)
            for participant in participants_json:
                new_person = Person(
                    participant,
                    participants_json[participant]["email"],
                    participants_json[participant]["invalid_matches"],
                )
                self.participants_dict[participant] = {
                    "email": participants_json[participant]["email"],
                    "invalid_matches": participants_json[participant][
                        "invalid_matches"
                    ],
                }
                participants.append(new_person)

        return participants

    def create_pairings(self):
        """
        Create optimal pairings between participants using a network flow approach.
        """
        graph = self._build_compatibility_graph()

        self.pairings = self._find_optimal_matching(graph)

        if not self.pairings:
            raise ValueError(
                "Could not generate valid Secret Santa pairings with current constraints."
            )

    def _build_compatibility_graph(self) -> dict[str, list[str]]:
        """
        Build a graph where each person is linked to all possible valid recipients.

        Returns
        -------
        dict[str, list[str]]
            A dictionary mapping each gifter to their list of potential giftees.
        """
        graph = {}

        for person in self.participants:
            valid_recipients = [
                other.name
                for other in self.participants
                if (
                    other.name != person.name
                    and other.name not in person.invalid_matches
                )
            ]
            graph[person.name] = valid_recipients

        return graph

    def _find_optimal_matching(self, graph: dict[str, list[str]]) -> dict[str, str]:
        """
        Find optimal matching using a backtracking approach.

        Parameters
        ----------
        graph : dict[str, list[str]]
            Compatibility graph between gifters and potential giftees.

        Returns
        -------
        dict[str, str]
            Dictionary mapping gifters to giftees.
        """
        all_participants = list(graph.keys())
        matching = {}

        def backtrack(index: int, assigned: set[str]) -> bool:
            # Base case: all participants have been assigned
            if index == len(all_participants):
                return True

            current_person = all_participants[index]
            # Shuffle potential recipients for variety
            potential_recipients = list(graph[current_person])
            random.shuffle(potential_recipients)

            for recipient in potential_recipients:
                if recipient in assigned:
                    continue

                matching[current_person] = recipient
                assigned.add(recipient)

                # Recursively try to assign remaining participants
                if backtrack(index + 1, assigned):
                    return True

                # Backtrack if this assignment didn't work
                matching.pop(current_person)
                assigned.remove(recipient)

            return False

        # Start backtracking from first participant
        success = backtrack(0, set())

        return matching if success else {}

    def add_new_pairings(self):
        """
        Add new pairings to the historical data.
        """
        pairings = pl.read_csv(HISTORY_FILE)

        new_rows = {
            "year": [datetime.now().year] * len(self.pairings.keys()),
            "gifter": [list(self.pairings.keys())],
            "giftee": [list(self.pairings.values())],
        }
        new_pairings = pl.DataFrame(new_rows)

        pairings.extend(new_pairings)

        pairings.write_csv(HISTORY_FILE)

    def update_invalid_matches(self):
        """
        Update the invalid_matches list in the participants dictionary.
        """
        for gifter, giftee in self.pairings.items():
            self.participants_dict[gifter]["invalid_matches"][-1] = giftee

        with open(PARTICIPANTS_FILE, "w") as json_file:
            json.dump(self.participants_dict, json_file, indent=2)
