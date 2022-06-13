class Request:
    def __init__(self, type: str, client_id: str, ticker: str):
        self.type = type
        self.client_id = client_id
        self.ticker = ticker
        self.index = -1
