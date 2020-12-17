from src.interface.ITrader import ITrader

class Trader(ITrader):

  def __init__(self, trader_id: str):
    self.__trader_id = trader_id

  def notify_partial_buy_order_execution(self, id: str, shares: int, price: float) -> None:
      """
      Override receive notification when partial buy order excute
      """
      print('Trader ID: {}, Your {} order(s) has been bought @ ${}'.format(
          self.__trader_id, shares, price))

  def notify_partial_sell_order_execution(self, id: str, shares: int, price: float) -> None:
      """
      Override receive notification when partial sell order excute
      """
      print('Trader ID: {}, Your {} order(s) has been sold @ ${}'.format(
          self.__trader_id, shares, price))