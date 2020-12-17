from src.models.Trader import Trader


class Order():

    def __init__(self, orginator: Trader, share: int, price: float):
        self.share = share
        self.price = price
        self.orginator = orginator

class BuyOrder(Order):

    def __init__(self, orginator: Trader, share: int, price: float):
        super().__init__(orginator, share, price)

    def resize_share(self, order_id: str, taken_share: int, price: float):
        self.orginator.notify_partial_buy_order_execution(order_id, taken_share, price)
        self.share -= taken_share

    def __str__(self):
        return 'Order Type: {}\nShare: {}\nPrice: ${:.4f}'.format('Buy', self.share, self.price)

class SellOrder(Order):

    def __init__(self, orginator: Trader, share: int, price: float):
        super().__init__(orginator, share, price)

    def resize_share(self, order_id: str, taken_share: int, price: float):
        self.orginator.notify_partial_sell_order_execution(order_id, taken_share, price)
        self.share -= taken_share

    def __str__(self):
        return 'Order Type: {}\nShare: {}\nPrice: ${:.4f}'.format('Sell', self.share, self.price)
