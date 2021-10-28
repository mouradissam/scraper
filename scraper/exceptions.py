class UnsupportedDataFeed(Exception):
    pass


class ExhaustedRetries(Exception):
    pass


class BadChecksum(Exception):
    pass


class ConnectionClosed(Exception):
    pass


class UnexpectedMessage(Exception):
    pass


class SearchError(Exception):
    pass
