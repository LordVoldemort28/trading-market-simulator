from src.abstract.ATrader import ATrader
from src.models.LvlOneScreen import LvlOneScreen
from src.models.ObservableOrderbook import ObservableOrderbook


class LvlOneTrader(ATrader):

    screen = LvlOneScreen()

    def __init__(self, observableOrderbook: ObservableOrderbook):
        observableOrderbook.register(self.screen)

    def time_slice(self) -> None:
        pass
