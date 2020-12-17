from src.interface import IOrderbookObserver


class MyScreen(IOrderbookObserver):

    def __init__(self):
        self.__best_bid: float
        self.__best_ask: float

    def notify_change(self) -> None:
        """
        Override notify change
        """
        pass
