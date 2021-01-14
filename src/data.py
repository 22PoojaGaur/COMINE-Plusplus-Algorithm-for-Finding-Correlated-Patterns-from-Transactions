from collections import OrderedDict


class Data(object):

    def __init__(self):
        self.supports = OrderedDict()
        self.transactions = []

    def read_data(self, filename):
        with open(filename, 'r') as fin:
            for trans in fin.readlines():
                t = trans.strip().split(';')
                self.transactions.append(t)

        # find support
        temp_supports = {}
        for trans in self.transactions:
            for item in trans:
                if item in temp_supports:
                    temp_supports[item] += 1
                else:
                    temp_supports[item] = 1

        sorted_item_tuples = sorted(temp_supports.items(), key=lambda item: item[1], reverse=True)

        for (item, count) in sorted_item_tuples:
            self.supports[item] = count
