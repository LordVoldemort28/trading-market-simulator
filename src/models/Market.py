from src.models.ObservableOrderbook import ObservableOrderbook
from src.models.LvlOneTrader import LvlOneTrader


class Market():

    observableOrderbook: ObservableOrderbook
    traders: list()

    def __init__(self, n_trader: int):
        self.observableOrderbook = ObservableOrderbook()

        for _ in range(n_trader):
            self.traders.append(LvlOneTrader(self.observableOrderbook))

    def time_slice(self) -> None:
        for trader in self.traders:
            trader.time_slice()
            self.observableOrderbook.process_order()
