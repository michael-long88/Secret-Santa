# Secret-Santa

Python script to assign, and then email, Secret Santa participants. Current iteration pulls emails from a user-created participants.yaml file. 

The script will assign a recipient to each participant based on an exlusion list in the participants.yaml file (example below). If the program is unable to find a valid, remaining participant to assign as the recipient after 10 tries, the pairings list will reset and start again. 

After the pairings has been completed, the program will then email each participant with the name of their Secret Santa.

# particpants.yaml 
Each participant will need to have their name listed in the invalid_matches list to prevent matching themselves. The actual file portion starts with and includes "---":

\---   
participant1:
  name: First Participant
  email: participant1@example.com
  invalid_matches: [First Participant]
participant2:
  name: Second Participant
  email: participant2@example.com
  invalid_matches: [Second Participant]
