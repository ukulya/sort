from abc import abstractmethod

from django.conf import settings
from django.core.mail import EmailMessage
from django.template import loader, Template

from info.models import PriceList


class BaseMailBuilder:
    TEMPLATE_NAME = None
    FROM_EMAIL = settings.EMAIL_HOST_USER

    @classmethod
    def get_template(cls):
        return cls.TEMPLATE_NAME

    @classmethod
    def _get_rendered_template(cls, context: dict, template: str = None) -> Template:
        if not template:
            template = cls.get_template()
        template = loader.get_template(template)
        return template.render(context)

    @classmethod
    @abstractmethod
    def build_message(cls, **kwargs) -> EmailMessage:
        """
        Method for building message template with provided kwargs
        :param kwargs: parameters for email
        :return: rendered email
        """


class OrderByEmailBuilder(BaseMailBuilder):
    TEMPLATE_NAME = 'emails/order_by_email.html'

    @classmethod
    def build_message(cls, recipient: str, text: str, email: str, file=None):
        data = {
            'text': text,
            'email': email,
        }
        template = cls._get_rendered_template(data)
        message = EmailMessage(
            subject='Заказ по почте!',
            body=template,
            to=[recipient],
            from_email=cls.FROM_EMAIL,
        )
        if file:
            message.attach_file(file.path, )
        message.content_subtype = 'html'
        return message


class SubscribeEmailBuilder(BaseMailBuilder):
    TEMPLATE_NAME = 'emails/subscribe.html'

    @classmethod
    def build_message(cls, recipient: str):
        data = {
        }
        template = cls._get_rendered_template(data)
        message = EmailMessage(
            subject='Спасибо за подписку',
            body=template,
            to=[recipient],
            from_email=cls.FROM_EMAIL,
        )
        message.content_subtype = 'html'
        return message


class PriceListEmailBuilder(BaseMailBuilder):
    TEMPLATE_NAME = 'emails/reseller-pricelist.html'

    @classmethod
    def build_message(cls, recipient: str, type: int):
        price_list = PriceList.objects.first()
        template = None
        file = None
        if price_list:
            if type == 0:
                file = price_list.reseller
            else:
                file = price_list.corporate
                template = 'emails/corporate-pricelist.html'
        data = {
        }
        template = cls._get_rendered_template(data, template)
        message = EmailMessage(
            subject='Спасибо за подписку',
            body=template,
            to=[recipient],
            from_email=cls.FROM_EMAIL,
        )
        if file:
            message.attach_file(file.path, )
        message.content_subtype = 'html'

        return message
