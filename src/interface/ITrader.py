from __future__ import annotations
from abc import ABC, abstractmethod


class ITrader(ABC):
    """
    The Trader interface declares the partial order execution method, used by Orderbook.
    """

    @abstractmethod
    def notify_partial_buy_order_execution(self, id: str, shares: int, price: float) -> None:
        """
        Receive notification when partial buy order excute
        """
        pass

    @abstractmethod
    def notify_partial_sell_order_execution(self, id: str, shares: int, price: float) -> None:
        """
        Receive notification when partial sell order excute
        """
        pass
