import uuid
import sys
from abc import ABC, abstractmethod
from sortedcontainers import SortedDict
from collections import OrderedDict
from src.interface.ITrader import ITrader
from src.models.Order import Order, BuyOrder, SellOrder
from src.utils import TimeUtils


class OrderBook(object):

    def __init__(self):
        self.buy: dict = SortedDict()
        self.sell: dict = SortedDict()
        self.order_map: dict = OrderedDict()

        self.orders: dict = {
            'buy': self.buy,
            'sell': self.sell,
        }

        print('Order book initiated at {}'.format(TimeUtils.get_current_time()))

    def submit_market_order(self,
                            originator: ITrader,
                            order_type: str,
                            shares: int,
                            price: float) -> str:
        """
        Process market buy and sell order

        Parameters
        ----------
        originator: ITrader
            identity of trader who originated the trader
        order_type: str
            order type either buy or sell
        share: int
            number of shares
        price: float
            price for which would like to trade

        Raise
        -------
        Invalid parameters
            if originator is none
            if order_type is not buy or sell
            if share is equal or less than 0
            if price is equal or less than 0

        Returns
        -------
        unique id to track order and cancel order
        """
        if originator == None:
            raise ValueError('Invalid originator')
        if order_type != 'buy' and order_type != 'sell':
            raise ValueError('Order type should be either buy or sell')
        if shares <= 0:
            raise ValueError('Shares should be greater than 0')
        if price <= 0:
            raise ValueError('Price should be greater than 0')

        order_id = str(uuid.uuid1())[:8]
        order = BuyOrder(originator, shares, price) if order_type == 'buy' else SellOrder(
            originator, shares, price)
        self.__add_order(order_id, order_type, order)

        # Notify all observer
        self.notify_allobservers('submit')

        return order_id

    def cancel_order(self, id: str) -> None:

        if id not in self.order_map.keys():
            print('Invalid order ID: {}'.format(id))
            return

        self.__remove_order(id)
        print('Order ID: {} is cancelled'.format(id))

    def track_order(self, id: str) -> str:
        if id not in self.order_map.keys():
            return 'Order doesn\'t exist or its completed'
        return 'Order ID: {}\n{}'.format(str(id), str(self.order_map[id]))

    def process_orders(self) -> None:

        while self.__transaction_condition():

            # Get max price on buying side and min price in selling side
            max_buy, min_sell = max(self.buy.keys()), min(self.sell.keys())

            # Get prices which can transact based on min sell and max buy
            buy_prices = list(
                filter(lambda price: price >= min_sell, list(self.buy)))
            sell_prices = list(
                filter(lambda price: price <= max_buy, list(self.sell)))

            # Pick the oldest buy and sell orders that can transact
            buy_order_id = self.__get_oldest_order('buy', buy_prices)
            sell_order_id = self.__get_oldest_order('sell', sell_prices)

            # Perform transaction
            self.__transact_order(buy_order_id, sell_order_id)

    def print_buy_sell_side(self) -> None:
        print('Buy Side: {}'.format(list(self.buy.keys())))
        print('Sell Side: {}'.format(list(self.sell.keys())))

    def __get_oldest_order(self, order_type: str, prices: list) -> str:

        if len(prices) <= 0:
            return

        min_value = sys.maxsize
        oldest_order_id = None
        for price in prices:
            for order_id, order in self.orders[order_type][price].items():
                if order.time < min_value:
                    min_value = order.time
                    oldest_order_id = order_id
        return oldest_order_id

    def __transaction_condition(self) -> bool:

        if len(self.buy) == 0 or len(self.sell) == 0:
            return False

        max_buy, min_sell = max(self.buy.keys()), min(self.sell.keys())
        return max_buy >= min_sell

    def __transact_order(self, buy_order_id: str, sell_order_id: str) -> None:
        orders_to_remove = set()
        buy_order = self.order_map[buy_order_id]
        sell_order = self.order_map[sell_order_id]

        if buy_order.share > sell_order.share:
            # Resize shares
            self.buy[buy_order.price][buy_order_id].resize_share(
                buy_order_id, sell_order.share, sell_order.price)
            self.sell[sell_order.price][sell_order_id].resize_share(
                sell_order_id, sell_order.share, buy_order.price)
            orders_to_remove.add(sell_order_id)
        elif buy_order.share == sell_order.share:
            # Resize shares
            self.sell[sell_order.price][sell_order_id].resize_share(
                sell_order_id, sell_order.share, buy_order.price)
            self.buy[buy_order.price][buy_order_id].resize_share(
                buy_order_id, buy_order.share, sell_order.price)
            orders_to_remove.add(sell_order_id)
            orders_to_remove.add(buy_order_id)
        elif buy_order.share < sell_order.share:
            # Resize shares
            self.sell[sell_order.price][sell_order_id].resize_share(
                buy_order_id, buy_order.share, sell_order.price)
            self.buy[buy_order.price][buy_order_id].resize_share(
                sell_order_id, buy_order.share, buy_order.price)
            orders_to_remove.add(buy_order_id)
        else:
            raise 'Error in processing order'

        # Notify all observer
        self.notify_allobservers('trade')

        # Removing orders after trade to fix mutation error
        for order_id in orders_to_remove:
            self.__remove_order(order_id)

    def __add_order(self, id: str, order_type: str, order: Order) -> None:

        # Add order in order map
        self.order_map[id] = order

        # Add order in sell and buy book
        if order.price in self.orders[order_type].keys():
            self.orders[order_type][order.price][id] = order
        else:
            self.orders[order_type][order.price] = OrderedDict({id: order})

    def __remove_order(self, id: str) -> None:

        if id not in self.order_map.keys():
            print('Invalid order ID: {}'.format(id))
            return

        # Remove valid order from order map
        order = self.order_map.pop(id)
        order_type = self.__get_order_type(order)

        # Remove valid order from buy and sell map
        self.orders[order_type][order.price].pop(id)

        # Remove price dict if no orders avaliable of that price
        if len(self.orders[order_type][order.price]) == 0:
            del self.orders[order_type][order.price]

    def __get_order_type(self, order: Order) -> str:
        return 'buy' if isinstance(order, BuyOrder) else 'sell'

    @abstractmethod
    def notify_allobservers(self, change: str) -> None:
        """
        Abstract method to all observer
        """
        pass
