import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
load_dotenv()
# print('postgres://postgres:admin@localhost/facturation'.replace("://", "ql://", 1))
#
# print(generate_password_hash("123456", method='sha256'))
from datetime import datetime
import random
import string
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


if __name__ == '__main__':
    mailBody('id7565', 'Dass')


