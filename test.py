import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.ehlo()

server.login('dassolution.service@gmail.com', os.environ['PASSWORD'])


me = "dassolution.service@gmail.com"
you = "maladealpha@gmail.com"

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "Link"
msg['From'] = me
msg['To'] = you

# Create the body of the message (a plain-text and an HTML version).
text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
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
            <td width="670" align="center"  bgcolor="#000131"><h1>Dassolution</h1></td>
          </tr>
          <tr>
            <td width="670" align="right" bgcolor="#000131"><p>November 2017</p></td>
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
                    <p>Bonjour Dass,</p> <br>
                    <p>Une demande de réinitialisation du mot de passe de votre compte Ynov a été effectuée le 01/10/2020 13:54:45.</p><br>
                    <p>Il vous suffit de cliquer sur le bouton ci-dessous pour accéder au formulaire vous permettant de définir votre nouveau mot de passe :</p><br>

                    <div id="divButton">
                        <a href="dassolution/reset/1/zejhgkbvqdjhgk3242jgze">
                            <button>Définir mon nouveau mot de passe</button>
                        </a>
                    </div><br>
                    <p>Ce lien de réinitialisation de mot de passe est valable jusqu'au 01/10/2020 14:54:45.</p><br>
                    <p>Si vous n'avez pas effectué cette demande, veuillez supprimer ce message.</p><br><br>
                    <div id="bye">
                        <p>Bien cordialement<br>Service Support Dassolution</p>
                    </div>

                </div>

            </td>
<!--            <td width="15"></td>-->
<!--            <td width="200" valign="top">-->
<!--              <h5>Introducing Haiku: Design and Create Motion</h5>-->
<!--              <p>With motion on the rise amongst web developers so too are the tools that help to streamline its creation. Haiku is a stand-alone..</p>-->
<!--            </td>-->
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

# Record the MIME types of both parts - text/plain and text/html.
# part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
# msg.attach(part1)
msg.attach(part2)

# Send the message via local SMTP server.
server.sendmail('dassolution.service@gmail.com', you, msg.as_string())
print("envoie reussi")
server.quit()