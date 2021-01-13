import logging
from os import environ

from email_helper import EmailNotifications

logger = logging.getLogger(__name__)
logger.setLevel(level='INFO')


def lambda_handler(event, context):
    account_number = event['account']

    s = EmailNotifications(
        mail_server="10.175.137.6",  # Set to IP for now as we have no DNS here
        sender="cec-notifications@sky.uk",
        logger=logger
    )

    s.send_html_email(
        subject="Hybrid AWS DNS Solution",
        recipients="mikael.michelier@sky.uk",
        html_template="./static/cec-dns-info.html",
        images=["./static/logo.png"],
        domain=event['detail']['tags']['resolved-by'],
        account_number=account_number
    )

