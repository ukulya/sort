EXCEPTION_MAPPER = {

}


class RequestExceptionHandlerMiddleware(object):

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    @staticmethod
    def process_exception(request, exception):
        error_class = EXCEPTION_MAPPER.get(exception.__class__.__name__, None)

        if error_class:
            return error_class({'message': exception.message}, safe=False)


class GeneralException(Exception):
    default_message = 'Something went wrong'

    def __init__(self, message=None):
        self.message = message if message else self.default_message


class EmailError(GeneralException):
    default_message = 'Error sending email'
