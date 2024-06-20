import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Paramètres de l'email


def send_mail(from_adress, to_adress, subject, body, password):
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
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {str(e)}")
    finally:
        server.quit()


from_address = "clement.perchais@live.fr"
to_address = "clement.perchais@live.fr"
subject = "Sujet de l'email"
body = "Bonjour, voici le corps de votre message."
password = ""
send_mail(from_address, to_address, subject, body, password)
