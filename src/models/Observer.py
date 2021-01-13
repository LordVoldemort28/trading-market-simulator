from src.interface.IOrderbookObserver import IOrderbookObserver
from src.models.OrderBook import OrderBook


class Observer(IOrderbookObserver):

    def __init__(self, observer_id: str):
        self.__observer_id = observer_id

    def notify_change(self, order_book: OrderBook, change: str) -> None:
        print('Observer ID: {} Notification: {}'.format(
            self.__observer_id, change))
