from src.models.OrderBook import OrderBook


class ATrader():

    def __init__(self, orderBook: OrderBook):
        self.orderBook = orderBook
