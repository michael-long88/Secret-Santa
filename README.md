# Secret-Santa

Python script to assign, and then email, Secret Santa participants. Current iteration pulls emails from a user-created `participants.json` file. 

The script will assign a recipient to each participant based on an exlusion list in the `participants.json` file (rename `participants.json.example` to `participants.json`). If the program is unable to find a valid, remaining participant to assign as the recipient after 10 tries, the pairings list will reset and start again. 

After the pairings has been completed, the program will then email each participant with the name of their Secret Santa. Pairings will be written to a csv with the year, the gifter, and the giftee.

The `secret_santa_emailer.py` script will email each participant with the name of their Secret Santa again, because people love to delete their emails even though they shouldn't. It's also useful for when Google decides to turn off "less secure apps" after you've already run the program and don't want to reassign matches by running the whole thing again.
