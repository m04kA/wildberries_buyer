class WildberriesApiClientException(IOError):
    def __init__(self, *args, **kwargs):
        super(WildberriesApiClientException, self).__init__(*args, **kwargs)


class ServerError(WildberriesApiClientException):
    """Ошибка в запросе"""
