import smtplib
from email.mime.text import MIMEText

from credentials import SENDER_EMAIL, HOST, SENDER_EMAIL_PWD


def send_email(to: str, subject: str, body: str):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = to
    msg["CC"] = SENDER_EMAIL
    e = smtplib.SMTP_SSL(host=HOST, port=465)

    e.login(SENDER_EMAIL, SENDER_EMAIL_PWD)
    e.sendmail(SENDER_EMAIL, [to,SENDER_EMAIL], msg.as_string())
    e.quit()
    print("EMAIL SENT {}".format(msg.as_string()))