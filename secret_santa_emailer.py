import smtplib
import ssl
import yaml
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


config = yaml.safe_load(open('email_config.yaml'))
port = config['PORT']
password = config['PASSWORD']
sender_email = config['SENDER_EMAIL']
participants_json = 'participants.json'
participants_dict = {}


with open(participants_json) as json_file:
    participants_json = json.load(json_file)
    for participant in participants_json:
        participants_dict[participant] = {
            'email': participants_json[participant]['email'],
            'match': participants_json[participant]['invalid_matches'][-1]
        }

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL(config['SMTP_SERVER'], port, context=context) as server:
    server.login(config['USERNAME'], password)

    for person, info in participants_dict.items():
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = info['email']
        message['Subject'] = f"Secret Santa drawing for {person}"
        body = f"Hello, {person}. \n\nYou have drawn {info['match']} for this year's " \
            f"Secret Santa."
        message.attach(MIMEText(body, 'plain'))
        text = message.as_string()
        print(f"Sending email to {person}...")
        server.sendmail(sender_email, info['email'], text)