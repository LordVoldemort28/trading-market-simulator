from src.interface.ITrader import ITrader
from src.models import OrderBook
from src.interface import ITrader


class MultiTraderOrderBook(OrderBook):

    def process_market_order(originator: ITrader, shares: int, price: float) -> None:
        """
        Process trade for multiple trader
        """
        trades = super().submit_market_order_buy(originator, shares, price)
        pass
