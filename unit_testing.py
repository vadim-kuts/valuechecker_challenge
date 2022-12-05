import unittest
import numpy as np

from compare_price import ProviderList, Provider

A = {
    '1': 0.9,
    '268': 5.1,
    '46': 0.17,
    '4620': 0.0,
    '468': 0.15,
    '4631': 0.15,
    '4673': 0.9,
    '46732': 1.1
    }

B = {
    '1': 0.92,
    '44': 0.5,
    '46': 0.2,
    '467': 1.0,
    '48': 1.2
    }

providers_list = ProviderList(['A', 'B'],[A, B])

class TestProvider(unittest.TestCase):
    def test_values(self):
        self.assertRaises(TypeError, Provider, {4: 3.0})
        self.assertRaises(TypeError, Provider, {'4': '3.0'})
        self.assertRaises(ValueError, Provider, {'four': 3.0})

class RoutingTest(unittest.TestCase):
    def test_values(self):
        self.assertRaises(TypeError, providers_list.compare_price, 26811049224)
        self.assertRaises(TypeError, providers_list.compare_price, 2681.1049224)
        self.assertRaises(ValueError, providers_list.compare_price, '26811O49224')

    def test_prices(self):
        test_cases = {
                '4631993728': ('A', 0.15),
                '4620476382': ('A', 0.0),
                '4673234772': ('B', 1.0),
                '4488429994': ('B', 0.5),
                '4648882934': ('A', 0.17),
                '2682948883': ('A', 5.1),
                '4672485993': ('A', 0.17),
                '1373487873': ('A', 0.9),
                '4673037422': ('A', 0.9),
                '4888839900': ('B', 1.2),
                '7787755567': (None, np.inf),
                '0002382666': (None, np.inf)
                    }

        for num, res in test_cases.items():
            self.assertEqual(providers_list.compare_price(num), res)
