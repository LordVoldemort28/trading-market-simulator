# imports
import pytest
from src.models.OrderBook import OrderBook
from src.interface.ITrader import ITrader


def test_orderbook_init():
    print('===================Test starts=================')
    ob = OrderBook()
    print('===================Test ends=================\n')


def test_case_1():
    print('===================Test starts=================')
    ITrader.__abstractmethods__ = set()

    p1 = ITrader()
    p2 = ITrader()
    p3 = ITrader()
    ob = OrderBook()
    print('{} is p1'.format(p1))
    print('{} is p2'.format(p2))
    print('{} is p3'.format(p3))
    print('===============================================')
    ob.submit_market_order(p1, 'buy', 2, 100)
    ob.submit_market_order(p2, 'buy', 10, 100)
    # noise condition
    ob.submit_market_order(p3, 'sell', 6, 100)
    print('===================Test ends=================\n')


def test_case_2():
    print('===================Test starts=================')
    ITrader.__abstractmethods__ = set()

    p1 = ITrader()
    p2 = ITrader()
    ob = OrderBook()
    print('{} is p1'.format(p1))
    print('{} is p2'.format(p2))
    print('===============================================')
    order_id = ob.submit_market_order(p1, 'buy', 10, 10)
    ob.submit_market_order(p1, 'buy', 10, 20)
    ob.submit_market_order(p1, 'buy', 10, 30)
    ob.submit_market_order(p1, 'buy', 10, 40)
    ob.submit_market_order(p1, 'buy', 10, 50)
    ob.submit_market_order(p2, 'sell', 10, 60)
    ob.submit_market_order(p2, 'sell', 10, 70)
    ob.submit_market_order(p2, 'sell', 10, 80)
    ob.submit_market_order(p2, 'sell', 10, 90)
    ob.submit_market_order(p2, 'sell', 10, 100)

    # noise condition
    ob.submit_market_order(p2, 'sell', 10, 33)
    print('===================Test ends=================\n')
