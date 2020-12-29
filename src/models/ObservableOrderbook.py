from src.models import OrderBook
from src.interface.IOrderbookObserver import IOrderbookObserver


class ObservableOrderbook(OrderBook):

    def __init__(self):
        self.__observers = list()

    def register(self, order_observer: IOrderbookObserver) -> None:
        self.__observers.append(order_observer)

    def deregister(self, order_observer: IOrderbookObserver) -> None:
        self.__observers.remove(order_observer)

    def notify_allobservers(self, change: str) -> None:
        """
        Override notify all observer
        """
        for observer in self.__observers:
            observer.notify_change(
                super(ObservableOrderbook, self),
                change
            )
