from __future__ import annotations
from abc import ABC, abstractmethod
from src.models import OrderBook


class IOrderbookObserver(ABC):
    """
    The Orderbook observer interface declares notify changes method, used by Orderbook.
    """

    @abstractmethod
    def notify_change(self, order_book: OrderBook, hint: str) -> None:
        """
        Receive notification when any changes happen in order book
        """
        pass
