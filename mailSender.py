import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
from datetime import datetime
import string
import random

load_dotenv()

def mailBody(id, name):
    dt_string = datetime.now()
    nextHour = dt_string.hour + 1
    if nextHour == 24:
        nextHour = '00'
    print(nextHour)
    expiredDate = dt_string.strftime('%d/%m/%Y hour:%M:%S').replace('hour', str(nextHour))
    characters = string.ascii_letters + string.digits
    token = ''.join(random.choice(characters) for i in range(20))
    return print(f"Bonjour {name}, \n\nUne demande de réinitialisation du mot de passe de votre compte Dassolution a "
                 f"été effectuée le {dt_string.strftime('%d/%m/%Y %H:%M:%S')}.\n"
                 f"Il vous suffit de cliquer sur le lien ci-après pour accéder au formulaire vous permettant de "
                 f"définir votre nouveau mot de passe : www.dassolution/organisations/reset/{id}/{token}\n\n"
                 f"Ce lien de réinitialisation de mot de passe est valable jusqu'au {expiredDate}."
                 f"\n\nBien cordialement\nService Support Dassolution")


def emailSender(mailReceive,body, sujet):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('dassolution.service@gmail.com', os.environ['PASSWORD'])

    msg = MIMEMultipart('alternative')
    msg['Subject'] = sujet
    msg['From'] = "dassolution.service@gmail.com"
    msg['To'] = mailReceive

    text = body

    part1 = MIMEText(text, 'plain')

    msg.attach(part1)

    server.sendmail('dassolution.service@gmail.com', mailReceive, msg.as_string())
    print("envoie reussi")
    server.quit()


if __name__ == '__main__':
    emailSender('heyy', 'Hey')
