from src.models.OrderBook import OrderBook


class LvlOneScreen(object):

    __price: float

    def __init__(self):
        pass

    def notify(self, orderBook: OrderBook, change: str) -> None:
        self.__price = (orderBook.get_max_buy() + orderBook.get_min_sell()) / 2

    def get_price(self) -> float:
        return self.__price
