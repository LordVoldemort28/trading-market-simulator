import uuid
from sortedcontainers import SortedDict
from collections import OrderedDict
from src.models.Trader import Trader
from src.models.Order import Order, BuyOrder, SellOrder
from src.utils import Time


class OrderBook():

    def __init__(self):
        self.buy: dict = SortedDict()
        self.sell: dict = SortedDict()
        self.order_map: dict = OrderedDict()

        self.orders: dict = {
            'buy': self.buy,
            'sell': self.sell,
        }

        print("Order book initiated at {}".format(Time.get_current_time()))

    def submit_market_order(self,
                            originator: Trader,
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
            max_buy, min_sell = max(self.buy.keys()), min(self.sell.keys())
            buy_prices = list(filter(lambda price: price >= min_sell, list(reversed(self.buy))))
            sell_prices = list(filter(lambda price: price <= max_buy, list(self.sell)))

            buy_price = buy_prices.pop(0)
            sell_price = sell_prices.pop(0)

            buy_order_id = list(self.buy[buy_price].keys()).pop(0)
            sell_order_id = list(self.sell[sell_price].keys()).pop(0)
            self.__transact_order(buy_order_id, sell_order_id)

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
            self.buy[buy_order.price][buy_order_id].resize_share(buy_order_id, sell_order.share, sell_order.price)
            self.sell[sell_order.price][sell_order_id].resize_share(sell_order_id, sell_order.share, buy_order.price)
            orders_to_remove.add(sell_order_id)
        elif buy_order.share == sell_order.share:
            # Resize shares
            self.sell[sell_order.price][sell_order_id].resize_share(sell_order_id, sell_order.share, buy_order.price)
            self.buy[buy_order.price][buy_order_id].resize_share(buy_order_id, buy_order.share, sell_order.price)
            orders_to_remove.add(sell_order_id)
            orders_to_remove.add(buy_order_id)
        elif buy_order.share < sell_order.share:
            # Resize shares
            self.sell[sell_order.price][sell_order_id].resize_share(buy_order_id, buy_order.share, sell_order.price)
            self.buy[buy_order.price][buy_order_id].resize_share(sell_order_id, buy_order.share, buy_order.price)
            orders_to_remove.add(buy_order_id)
        else:
            raise "Error in processing order"
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