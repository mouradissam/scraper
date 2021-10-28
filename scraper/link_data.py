class LinkData:
    def __init__(self, data: str, timestamp=None, receipt_timestamp=None) -> None:
        self.data = data
        self.timestamp = timestamp
        self.receipt_timestamp = receipt_timestamp
