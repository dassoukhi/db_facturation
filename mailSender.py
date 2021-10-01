import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()


def emailSender(message, sujet):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('dassolution.service@gmail.com', os.environ['PASSWORD'])

    msg = MIMEMultipart('alternative')
    msg['Subject'] = sujet
    msg['From'] = "dassolution.service@gmail.com"
    msg['To'] = 'dassolution.service@gmail.com'

    text = message

    part1 = MIMEText(text, 'plain')

    msg.attach(part1)

    server.sendmail('dassolution.service@gmail.com', 'dassolution.service@gmail.com', msg.as_string())
    print("envoie reussi")
    server.quit()


if __name__ == '__main__':
    emailSender('heyy', 'Hey')
