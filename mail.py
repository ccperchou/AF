import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def send_mail(from_adress, to_adress, subject, body, password):
    """
    Sends an email using the SMTP protocol.

    Parameters:
    - from_address (str): The email address of the sender.
    - to_address (str): The email address of the recipient.
    - subject (str): The subject of the email.
    - body (str): The body of the email.
    - password (str): The password of the sender's email account.

    Returns:
    int: 400 if the email is sent successfully, 500 otherwise.
    """
    # Création de l'objet MIMEMultipart
    msg = MIMEMultipart()
    msg["From"] = from_adress
    msg["To"] = to_adress
    msg["Subject"] = subject

    # Attachement du corps de l'email
    msg.attach(MIMEText(body, "plain"))

    # Connexion au serveur SMTP Outlook et envoi de l'email
    try:
        server = smtplib.SMTP("smtp.office365.com", 587)
        server.starttls()
        server.login(from_adress, password)
        text = msg.as_string()
        server.sendmail(from_adress, to_adress, text)
        print("Email envoyé avec succès!")
        return 400
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {str(e)}")
        return 500
    finally:
        server.quit()


""" 
from_address = "clement.perchais@live.fr"
to_address = "clement.perchais@live.fr"
subject = "Sujet de l'email"
body = "Bonjour, voici le corps de votre message."
password = " "
send_mail(from_address, to_address, subject, body, password)
"""
