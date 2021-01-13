import pytest
from src.models.ObservableOrderbook import ObservableOrderbook
from src.models.Trader import Trader
from src.models.Observer import Observer


def test_observableOrderbook():

    p1 = Trader('P1')
    p2 = Trader('P2')
    p3 = Trader('P3')
    observer = Observer('observer1')
    ob = ObservableOrderbook()

    ob.register(observer)
    ob.submit_market_order(p1, 'buy', 2, 100)
    ob.submit_market_order(p2, 'buy', 10, 100)

    # noise condition
    ob.submit_market_order(p3, 'sell', 6, 100)
    ob.process_orders()
