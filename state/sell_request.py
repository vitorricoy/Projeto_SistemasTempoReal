import decimal
from state.request import Request


class SellRequest(Request):
    def __init__(self, client_id: str, ticker: str, min_price: decimal.Decimal):
        super().__init__('SELL', client_id, ticker)
        self.min_price = min_price
