from abc import ABCMeta, abstractmethod


class BaseErrorException(Exception, metaclass=ABCMeta):
    def __init__(self, message: str = None):
        super().__init__()
        self._message = message

    @property
    @abstractmethod
    def default_message(self):
        pass

    @property
    def message(self):
        return self._message or self.default_message


class MessageDoesNotSend(BaseErrorException):
    default_message = 'Сообщение не было доставлено'


class ObjectDoesNotExistException(BaseErrorException):
    default_message = 'Объект с предоставленными не найден'


class WrongTokenException(BaseErrorException):
    default_message = "Неверный формат токена"


class KeyErrorException(BaseErrorException):
    default_message = "Неправильные данные"
