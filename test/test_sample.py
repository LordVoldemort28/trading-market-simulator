# imports
import pytest
from src.models.OrderBook import OrderBook
from src.models.Trader import Trader


def test_orderbook_init():
    print('===================Test Case 1=================')
    ob = OrderBook()
    print('===================Test ends=================\n')

def test_case():
    print('===================Test Case 2=================')

    trader = Trader('Trader')
    ob = OrderBook()
    ob.submit_market_order(trader, 'buy', 5, 66)
    ob.submit_market_order(trader, 'buy', 5, 67)
    ob.submit_market_order(trader, 'buy', 5, 68)
    ob.submit_market_order(trader, 'buy', 5, 69)
    ob.submit_market_order(trader, 'buy', 5, 70)
    ob.submit_market_order(trader, 'sell', 5, 71)
    ob.submit_market_order(trader, 'sell', 5, 72)
    ob.submit_market_order(trader, 'sell', 5, 73)
    ob.submit_market_order(trader, 'sell', 5, 74)
    ob.submit_market_order(trader, 'sell', 5, 75)

    # noise conditions
    ob.submit_market_order(trader, 'buy', 5, 76)
    ob.submit_market_order(trader, 'buy', 5, 73.5)
    ob.submit_market_order(trader, 'buy', 5, 72.5)
    ob.process_orders()
    print('===================Test ends=================\n')

def test_case_1():
    print('===================Test Case 3=================')

    p1 = Trader('P1')
    p2 = Trader('P2')
    p3 = Trader('P3')
    ob = OrderBook()
    ob.submit_market_order(p1, 'buy', 2, 100)
    ob.submit_market_order(p2, 'buy', 10, 100)

    # noise condition
    ob.submit_market_order(p3, 'sell', 6, 100)
    ob.process_orders()
    print('===================Test ends=================\n')


def test_case_2():
    print('===================Test Case 4=================')

    p1 = Trader('P1')
    p2 = Trader('P2')
    ob = OrderBook()
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
    ob.process_orders()
    print('===================Test ends=================\n')
