import logging

from mailer.builders import OrderByEmailBuilder, SubscribeEmailBuilder, PriceListEmailBuilder
from mailer.senders import EmailSender

logger = logging.getLogger(__name__)


class MailerService:
    @classmethod
    def send_order_email(cls, recipient: str, text: str, email: str, file: str = None):
        message = OrderByEmailBuilder.build_message(recipient, text, email, file)
        email_sender = EmailSender([message])
        email_sender.start()
        logger.info(f'Sent order email to {recipient}')

    @classmethod
    def send_subscriber_email(cls, recipient: str):
        message = SubscribeEmailBuilder.build_message(recipient)
        email_sender = EmailSender([message])
        email_sender.start()
        logger.info(f'Sent subscribe email to {recipient}')

    @classmethod
    def send_price_list(cls, recipient: str, type: int):
        message = PriceListEmailBuilder.build_message(recipient, type)
        email_sender = EmailSender([message])
        email_sender.start()
        logger.info(f'Sent price list email to {recipient}')
