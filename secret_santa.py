import random
import smtplib
import ssl
import yaml
import json
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


class Person:
    def __init__(self, name, email, invalid_match):
        self.name = name
        self.email = email
        self.invalid_match = invalid_match

    def __str__(self):
        return f"{self.name}, {self.email}"


class SecretSanta:
    def __init__(self):
        self.pairings = {}
        self.recipient_check = 0
        self.participants_dict = {}
        self.pairings_csv = 'pairings.csv'
        self.participants_json = 'participants.json'
        self.participants = self.get_participants()

    def get_participants(self) -> list:
        participants = []
        with open(self.participants_json) as json_file:
            participants_json = json.load(json_file)
            for participant in participants_json:
                new_person = Person(participant, participants_json[participant]['email'], participants_json[participant]['invalid_matches'])
                self.participants_dict[participant] = {
                    'email': participants_json[participant]['email'],
                    'invalid_matches': participants_json[participant]['invalid_matches']
                }
                participants.append(new_person)
        return participants

    def create_pairings(self):
        index = 0
        while len(self.pairings.keys()) != len(self.participants):
            current_participant = self.participants[index]
            recipient = self.get_recipient(current_participant)
            if current_participant.name == recipient.name:
                self.pairings = {}
                index = 0
            else:
                self.pairings[current_participant.name] = recipient.name
                index += 1

    def get_recipient(self, giver: Person) -> Person:
        if self.participants[-1].name == giver.name:
            assigned_recipients = list(secret_santa.pairings.values())
            remaining_person = [person for person in self.participants if person.name not in assigned_recipients]
            self.recipient_check = 0
            return remaining_person[0]

        if self.recipient_check > 10:
            self.recipient_check = 0
            return giver
        random.seed()
        random_number = random.randint(0, len(self.participants) - 1)
        if self.participants[random_number].name in giver.invalid_match or \
                self.participants[random_number].name in self.pairings.values():
            self.recipient_check += 1
            return self.get_recipient(giver)
        self.recipient_check = 0
        return self.participants[random_number]

    # https://realpython.com/python-send-email/
    def send_emails(self):
        config = yaml.safe_load(open('email_config.yaml'))
        port = config['PORT']
        password = config['PASSWORD']
        sender_email = config['SENDER_EMAIL']

        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(config['SMTP_SERVER'], port, context=context) as server:
            server.login(config['USERNAME'], password)

            for person in self.participants:
                message = MIMEMultipart()
                message['From'] = sender_email
                message['To'] = person.email
                message['Subject'] = f"Secret Santa drawing for {person.name}"
                body = f"Hello, {person.name}. \n\nYou have drawn {self.pairings[person.name]} for this year's " \
                    f"Secret Santa."
                message.attach(MIMEText(body, 'plain'))
                text = message.as_string()
                print(f"Sending email to {person.name}...")
                server.sendmail(sender_email, person.email, text)

    def add_new_pairings(self):
        pairings_df = pd.read_csv(self.pairings_csv)
        new_rows = {
            'year': [datetime.now().year] * len(self.pairings.keys()),
            'gifter': [],
            'giftee': []
        }
        for giver, receiver in self.pairings.items():
            new_rows['gifter'].append(giver)
            new_rows['giftee'].append(receiver)
        pairings_df = pairings_df.append(pd.DataFrame.from_dict(new_rows), ignore_index=True)
        pairings_df.to_csv(self.pairings_csv, index=False)

    def update_invalid_matches(self):
        for gifter, giftee in self.pairings.items():
            self.participants_dict[gifter]['invalid_matches'][-1] = giftee
        with open(self.participants_json, 'w') as json_file:
            json.dump(self.participants_dict, json_file, indent=2)


if __name__ == '__main__':
    secret_santa = SecretSanta()
    secret_santa.create_pairings()
    secret_santa.add_new_pairings()
    secret_santa.update_invalid_matches()
    secret_santa.send_emails()
