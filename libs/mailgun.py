import os
from typing import List
from requests import Response, post


class MailgunException(Exception):
    def __init__(self, message):
        self.message = message


class Mailgun:
    MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY', None)
    MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN', None)

    FROM_TITLE = "Price alert"
    FROM_EMAIL = "do-not-reply@sandbox4efc4072d5a748838de4fcc2725196aa.mailgun.org"

    @classmethod
    def send_mail(cls, email: List[str], subject: str, text: str, html: str) -> Response:
        if not cls.MAILGUN_API_KEY:
            raise MailgunException('Failed to load Mailgun API key.')

        if not cls.MAILGUN_DOMAIN:
            raise MailgunException('Failed to load Mailgun domain.')

        response = post(
            f"{cls.MAILGUN_DOMAIN}/messages",
            auth=("api", cls.MAILGUN_API_KEY),
            data={"from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                  "to": email,
                  "subject": subject,
                  "text": text,
                  "html": html})
        if response.status_code != 200:
            print(response.json())
            raise MailgunException('An error occurred while sending e-mail')
        return response
