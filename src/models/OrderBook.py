import uuid
from sortedcontainers import SortedDict
from collections import OrderedDict
from src.interface import ITrader
from src.models.Order import Order, BuyOrder, SellOrder
from src.utils import Time


class OrderBook(ITrader):

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
        return order_id

    def cancel_order(self, id: str) -> None:

        if id not in self.order_map.keys():
            print('Invalid order ID: {}'.format(id))
            return

        self.__remove_order(id)
        print('Order ID: {} is cancelled'.format(id))

    def track_order(self, id: str) -> None:
        print('Order ID: {}\n{}'.format(str(id), self.order_map[id].info))

    def __process_order(self, order_type: str, order_id: str) -> None:

        order = self.order_map[order_id]
        op_order_type = 'buy' if order_type == 'sell' else 'sell'
        match_prices = self.__get_match_prices(order_type, order.price)

        orders_to_remove = set()
        while match_prices and order.share > 0:
            match_price = match_prices.pop(0)
            for match_order_id, match_order in self.orders[op_order_type][match_price].items():
                if order.share > 0:
                    if match_order.share > order.share:
                        self.orders[op_order_type][match_price][match_order_id].resize_share(
                            order.share)
                        order.resize_share(order.share)
                        orders_to_remove.add(order_id)
                    elif match_order.share == order.share:
                        order.resize_share(order.share)
                        self.orders[op_order_type][match_price][match_order_id].resize_share(
                            match_order.share)
                        orders_to_remove.add(order_id)
                        orders_to_remove.add(match_order_id)
                    elif order.share > match_order.share:
                        order.resize_share(match_order.share)
                        self.orders[op_order_type][match_price][match_order_id].resize_share(
                            match_order.share)
                        orders_to_remove.add(match_order_id)
                    else:
                        raise "Error in processing order"
                else:
                    break
        # Removing orders after trade to fix mutation error
        for order_id in orders_to_remove:
            self.__remove_order(order_id)
        return

    def notify_partial_buy_order_execution(self, id: str, order: Order) -> None:
        """
        Override receive notification when partial buy order excute
        """
        print('{}, Your {} order(s) has been fulfilled'.format(
            id, order.share))

    def notify_partial_sell_order_execution(self, id: str, order: Order) -> None:
        """
        Override receive notification when partial sell order excute
        """
        print('{}, Your {} order(s) has been sold'.format(
            id, order.share))

    def __add_order(self, id: str, order_type: str, order: Order) -> None:
        self.order_map[id] = order
        if order.price in self.orders[order_type].keys():
            self.orders[order_type][order.price][id] = order
        else:
            self.orders[order_type][order.price] = OrderedDict({id: order})

    def __remove_order(self, id: str) -> None:

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

    def __get_orders(self, order_type: str, price: float) -> OrderedDict:
        return self.orders[order_type][price]

    def __get_match_prices(self, order_type: str, price: float):
        if order_type == 'buy':
            # Return all prices in sell side that are equal or less than buying price
            return [sell for sell in self.sell.keys() if sell <= price]
        elif order_type == 'sell':
            # Return all prices in buy side that are equal or more than selling price
            return [buy for buy in self.buy.keys() if buy >= price]
        else:
            return []
