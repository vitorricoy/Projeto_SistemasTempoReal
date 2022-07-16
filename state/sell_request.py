import decimal
from state.request import Request


class SellRequest(Request):
    def __init__(self, client_id: str, ticker: str, min_price: decimal.Decimal):
        super().__init__('SELL', client_id, ticker)
        self.min_price = min_price

    def __repr__(self) -> str:
        return f"{super().__repr__()}, min_price={self.min_price}"
