class Request:
    def __init__(self, type: str, client_id: str, ticker: str):
        self.type = type
        self.client_id = client_id
        self.ticker = ticker
        self.index = -1
    
    def __repr__(self) -> str:
        return f"Type={self.type}, ClientId={self.client_id}, Ticker={self.ticker}, Index={self.index}"
