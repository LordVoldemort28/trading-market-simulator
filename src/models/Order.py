from src.interface import ITrader


class Order:

    def __init__(self, orginator: ITrader, share: int, price: float):
        self.share = share
        self.price = price
        self.orginator = orginator

    def resize_share(self, place_order: int):
        print('{}, Your {} order(s) has been fulfilled'.format(
            self.orginator, place_order))
        self.share -= place_order


class BuyOrder(Order):

    def __init__(self, orginator: ITrader, share: int, price: float):
        super().__init__(orginator, share, price)
        self.info = 'Order Type: {}\n \
                    Share: {}\n \
                    Price: ${:.4f}'.format('Buy', self.share, self.price)


class SellOrder(Order):

    def __init__(self, orginator: ITrader, share: int, price: float):
        super().__init__(orginator, share, price)
        self.info = 'Order Type: {}\n \
                    Share: {}\n \
                    Price: ${:.4f}'.format('Sell', self.share, self.price)
