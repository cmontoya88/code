import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

# from app.params import smtp_serv, smtp_port, smtp_domain, smtp_user, smtp_pass, notify

smtp_serv = 'smtp.gmail.com'
smtp_port = '587'
smtp_domain = 'gmail.com'
smtp_user = 'cmontoya88'  # Requiere se habilite SMTP en Gmail
smtp_pass = 'contraseña'
notify = '1'


def mailing(subject='', body='', to='', cc='', bcc='', filepath=None, is_tls=True):

    msg = MIMEMultipart()

    account = smtp_user + '@' + smtp_domain
    msg['From'] = account

    msg['To'] = to
    msg['Cc'] = cc
    msg['Bcc'] = bcc

    msg['Subject'] = subject
    # msgText = MIMEText('<b>%s</b>' % body, 'html')
    msgText = MIMEText(body, 'html')
    msg.attach(msgText)

    if filepath is not None:

        base = os.path.basename(filepath)
        filename, extension = os.path.splitext(base)

        if extension == ".txt":
            msg.attach(MIMEText(open(filepath).read()))

        elif extension == ".jpg":
            with open(filepath, 'rb') as fp:
                img = MIMEImage(fp.read())
                img.add_header('Content-Disposition', 'attachment', filename=filename)
                msg.attach(img)

        else:  # pdf, xlsx, etc
            fileMIMEApplication = MIMEApplication(open(filepath, 'rb').read(), Name=filename)
            fileMIMEApplication.add_header('Content-Disposition', 'attachment', filename=filename)
            msg.attach(fileMIMEApplication)

    try:
        with smtplib.SMTP(smtp_serv, smtp_port) as smtpObj:
            smtpObj.ehlo()
            if is_tls:
                smtpObj.starttls()
            smtpObj.login(smtp_user, smtp_pass)
            # smtpObj.sendmail(account, to, msg.as_string())
            if bool(int(notify)):
                smtpObj.send_message(msg)
            smtpObj.quit()
    except Exception as e:
        print('ERROR MAILING')
        print(e)


# Envío con asunto, contenido (puede ser html), destinatario
mailing('Prueba', 'Esta es una prueba CODE', 'cmontoya88@gmail.com')
