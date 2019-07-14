import random
import smtplib
import ssl
import yaml
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
        self.participants = SecretSanta.get_participants()
        self.pairings = {}
        self.recipient_check = 0

    @staticmethod
    def get_participants() -> list:
        participants = []
        with open('participants.yaml') as f:
            participants_yaml = yaml.safe_load(f)
            for participant in participants_yaml.values():
                new_person = Person(participant['name'], participant['email'], participant['invalid_matches'])
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
            assigned_recipients = [recipient for recipient in secret_santa.pairings.values()]
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
                message['Subject'] = "Secret Santa drawing"
                body = f"Hello, {person.name}. \n\nYou have drawn {self.pairings[person.name]} for this year's " \
                    f"Secret Santa."
                message.attach(MIMEText(body, 'plain'))
                text = message.as_string()
                print("Sending emails...")
                server.sendmail(sender_email, person.email, text)


if __name__ == '__main__':
    secret_santa = SecretSanta()
    secret_santa.create_pairings()
    log_config = yaml.safe_load(open('log_config.yaml'))
    with open(f"{log_config['PATH']}/pairings.txt", "a") as f:
        f.write(f"------------------------------------{datetime.now().year}------------------------------------\n")
        for gifter, giftee in secret_santa.pairings.items():
            f.write(f"{gifter}, {giftee}\n")
        f.write("\n\n")
    secret_santa.send_emails()
