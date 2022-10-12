from asyncio import SendfileNotAvailableError
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import libs

class EmailTool:

    def __init__(self, server, port, sender, receivers=[], startls=True, token=None):
        self._server = server
        self._port = port
        self._sender = sender
        self._receivers = receivers
        self._starttls = startls
        self._token = token
        self._message = MIMEMultipart()

    def send(self):
        try:
            session = smtplib.SMTP(self._server, self._port)
            session.ehlo()
            if self._starttls:
                session.starttls()
            session.ehlo()
            session.login(self._sender, self._token)
            session.sendmail(self._sender, self._receivers, self._message.as_string())
        except Exception as e:
            libs.log_error("Failed to Send email")
            libs.log_error(e)
        finally:
            session.quit()

        libs.log_info("Email sent successfully")

    def set_token(self, token):
        self._token = token
        libs.log_info("Email Token is updated")

    def update_header(self, headers):
        for key, value in headers.items():
            self._message.add_header(key, value)

    def compose(self, title, body, headers):
        self._message['From'] = self._sender
        self._message['Subject'] = title
        self._message.attach(MIMEText(body, 'plain'))
        self.update_header(headers)

        libs.log_debug(f"EMAIL Message: \n{self._message}")