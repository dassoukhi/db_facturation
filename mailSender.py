import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
from datetime import datetime
import string
import random

load_dotenv()
EMAIL = 'dassolution.service@gmail.com'

def mailBody(id, name):
    dt_string = datetime.now()
    nextHour = dt_string.hour + 1
    if nextHour == 24:
        nextHour = '00'
    expiredDate = dt_string.strftime('%d/%m/%Y hour:%M:%S').replace('hour', str(nextHour))
    characters = string.ascii_letters + string.digits
    token = ''.join(random.choice(characters) for i in range(20))
    html = """\
    <!DOCTYPE html
    <html>
      <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
       <title>Tutsplus Email Newsletter</title>
       <style type="text/css">
        a {color: #d80a3e;}
      body, #header h1, #header h2, p {margin: 0; padding: 0;}
      div {padding: 30; height: 100vh; margin: 20px;}
      #divButton {display: flex; justify-content: center;  align-items: center; height: 50px;}
      #bye {display: flex; justify-content: flex-end;  align-items: center; height: 40px; margin-right: -15px;}
      #main {border: 1px solid #cfcece;}
      img {display: block;}
      #top-message p, #bottom p {color: #3f4042; font-size: 12px; font-family: Arial, Helvetica, sans-serif; }
      #header h1 {color: #ffffff !important; font-family: "Lucida Grande", sans-serif; font-size: 24px; margin-bottom: 0!important; padding-bottom: 0; }
      #header p {color: #ffffff !important; font-family: "Lucida Grande", "Lucida Sans", "Lucida Sans Unicode", sans-serif; font-size: 12px;  }
      h5 {margin: 0 0 0.8em 0;}
        h5 {font-size: 18px; color: #444444 !important; font-family: Arial, Helvetica, sans-serif; }
      p {font-size: 14px; color: #444444 !important; font-family: "Lucida Grande", "Lucida Sans", "Lucida Sans Unicode", sans-serif; line-height: 1.5;}
      button {background-color: #fb2e59; border: none; border-radius: 5px; height: 50px; width: 400px; color: white;}
       </style>
      <body>
    <table width="100%" cellpadding="0" cellspacing="0" bgcolor="e4e4e4"><tr><td>
    <table id="main" width="100vw" align="center" cellpadding="0" cellspacing="15" bgcolor="ffffff">
        <tr>
          <td>
            <table id="header" cellpadding="10" cellspacing="0" align="center" bgcolor="8fb3e9">
              <tr>
                <td width="670" align="center"  bgcolor="#000131"><h1>Dass~olution</h1></td>
              </tr>
              <tr>
                <td width="670" align="right" bgcolor="#000131"><p>"""+str(dt_string.year)+"""</p></td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td>
            <table id="content-4" cellpadding="0" cellspacing="0" align="center">
              <tr>
                <td width="600" height="500"  valign="top" bgcolor="#eee" cellpadding="30" >
                    <div>
                        <p>Bonjour """+name+""",</p> <br>
                        <p>Une demande de réinitialisation du mot de passe de votre compte a été effectuée le """+dt_string.strftime('%d/%m/%Y %H:%M:%S')+""".</p><br>
                        <p>Il vous suffit de cliquer sur le bouton ci-dessous pour accéder au formulaire vous permettant de définir votre nouveau mot de passe :</p><br>

                        <div id="divButton">
                            <a href='http://www.dassolution.fr/reset/"""+str(id) +'/'+ token+"""'>
                                <button>Définir mon nouveau mot de passe</button>
                            </a>
                        </div><br>
                        <p>Ce lien de réinitialisation de mot de passe est valable jusqu'au """+str(expiredDate)+""".</p><br>
                        <p>Si vous n'avez pas effectué cette demande, veuillez supprimer ce message.</p><br><br>
                        <div id="bye">
                            <p>Bien cordialement<br>Service Support Dassolution</p>
                        </div>
                    </div>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
      <table id="bottom" cellpadding="20" cellspacing="0" width="600" align="center">
        <tr>
          <td align="center">
            <p><a href="#">Se désinscrire</a> | <a href="#">Tweet</a> | <a href="#">Ouvrir dans navigateur</a></p>
          </td>
        </tr>
      </table><!-- top message -->
    </td></tr></table><!-- wrapper -->
    </body>
    </html>
    """
    return html


def emailSender(mailReceive,body, sujet):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(EMAIL, os.environ['PASSWORD'])

    msg = MIMEMultipart('alternative')
    msg['Subject'] = sujet
    msg['From'] = EMAIL
    msg['To'] = mailReceive

    html = body

    part1 = MIMEText(html, 'html')

    msg.attach(part1)

    server.sendmail(EMAIL, mailReceive, msg.as_string())
    print("envoie reussi")
    server.quit()


if __name__ == '__main__':
    emailSender('maladealpha@gmail.com', mailBody(1, 'Saleh'),'Dassolution | Réinitialisation de votre mot de passe')
