import logging
logging.basicConfig(filename='../data/run.log', level=logging.DEBUG)

import get_frequent_items
import sys
from collections import OrderedDict
import copy
import pprint
import comine_k
from tree import Tree
from data import Data
import globals




def sort_transaction(trans, item_count_dict):
    """
    trans: (list) transaction.
    item_count_dict: (dict) dictionary containing item vs support for item.
    """
    trans_dict = {}

    for item in trans:
        if item_count_dict[item] >= globals.MIN_SUPPORT:
            trans_dict[item] = item_count_dict[item]

    trans_dict = OrderedDict(
        sorted(trans_dict.items(), key=lambda val: val[1], reverse=True))

    return list(trans_dict.keys())


if __name__ == '__main__':
    # initialize Data class
    D = Data()
    D.read_data(sys.argv[1])

    # print ("Supports ")
    # pprint.pprint(D.supports)

    # initialize tree
    T = Tree()

    sorted_frequent_item = []
    for trans in D.transactions:
        sorted_trans = sort_transaction(trans, D.supports)
        print("processing transaction ", ' '.join(sorted_trans))
        T.insert_transaction(sorted_trans)

    T.print()

    # print('\n\nNode to item')
    # pprint.pprint(T.node_to_item)

    print('\n\nHeader of tree')
    pprint.pprint(T.header)

    # for v in T.header.items():
    #     print (v[0])
    #     print (sum([int(n.node_count) for n in v[1]]))
    #
    # it = sorted(T.header.items(), key=lambda v: sum([int(n.node_count) for n in v[1]]))

    # print(it)

    # print ("List of all nodes")
    # print (T.get_all_nodes())

    comine_k.cominek(T, suffix=None, k=1, data=D)

