import os
import warnings
import numpy as np
import re
import argparse
import csv
from argparse import ArgumentParser


def file_to_dict(file):
    f = csv.reader(open(file, 'r'))
    out = {}
    for row in f:
        k, v = row
        out[k] = float(v)
    return out


def check_num(num):
    return not bool(re.compile(r'[^z0-9]').search(num))


class Provider(object):

    def compare_price(self, num):
        if type(num) != str:
            raise TypeError('the number variable is not string')
        if not check_num(num):
            raise ValueError('the number must consists of digits')
        if len(num) == 0:
            warnings.warn('The number is too short')
            return self.price
        elif num[0] not in self._sub_providers.keys():
            return self.price
        else:
            price = self._sub_providers[num[0]].compare_price(num[1:])

            if np.isinf(price):
                return self.price
            else:
                return price

    def __init__(self, pricelist):
        for prefix, price in pricelist.items():
            if type(prefix) != str:
                raise TypeError('keys are not strings.')
            if not check_num(prefix):
                raise ValueError('keys must consists of digits.')
            if type(price) != float:
                raise TypeError('prices must be float numbers.')
        self._sub_providers = {}
        if '' in pricelist.keys():
            self.price = pricelist['']
        else:
            self.price = np.inf
        for i in range(10):
            i = str(i)
            new_pricelist = {prefix[1:]: price
                              for prefix, price in pricelist.items()
                              if prefix.startswith(i)}
            if len(new_pricelist) > 0:
                self._sub_providers[i] = Provider(new_pricelist)



class ProviderList(object):

    def compare_price(self, num):
        prices = np.array([op.compare_price(num) for op in self.providers])
        if np.any(~np.isinf(prices)):
            k = np.argmin(prices)
            return self.names[k], prices[k]
        else:
            return None, np.inf


    def __init__(self, names, pricelists):
        self.names = names
        self.providers = [Provider(pl) for pl in pricelists]


def main():
    parser = ArgumentParser()
    parser.add_argument('number', type=str)
    parser.add_argument('--pricelist-path', type=str, default='pricelists')
    parser.add_argument('--providers', type=str, default=None, nargs='+')
    args = parser.parse_args()
    if args.providers is None:
        args.providers = [os.path.join(args.pricelist_path, filename)
                          for filename in os.listdir(args.pricelist_path)]
    if len(args.providers) == 0:
        raise ValueError("there are no files in pricelist directory")
    names = [fn.split('/')[-1][:-4] for fn in args.providers]
    pricelists = [file_to_dict(fn) for fn in args.providers]
    provider_list = ProviderList(names, pricelists)
    result = provider_list.compare_price(args.number)
    if result[0] is not None:
        print('Cheapest price for number ' + f'{args.number} is ${result[1]:.2f}/min with operator {result[0]}')
    else:
        print('The number ' + f'{args.number}' + ' cannot be dialed')


if __name__ == '__main__':
    main()
