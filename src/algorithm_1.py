import get_frequent_items
import sys
from collections import OrderedDict
import copy
import pprint
import comine_k
from tree import Tree
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
    fin = open(sys.argv[1], 'r')

    (item_count_dict, data) = get_frequent_items.get_frequent_item_count_dict(fin)

    # initialize tree
    T = Tree()
    for k in item_count_dict.keys():
        T.header[k] = []
    T.item_counts = item_count_dict

    sorted_frequent_item = []
    # Root
    for trans in data:
        sorted_trans = sort_transaction(trans, item_count_dict)
        # print (sorted_trans)
        T.insert_tree(sorted_trans[0], sorted_trans[1:], 0)
        # print ('\n')

    pprint.pprint(T.T)

    print ('\n\nNode to item')
    pprint.pprint (T.node_to_item)

    print ('\n\nHeader of tree')
    pprint.pprint (T.header)

    comine_k.cominek(T, None, 1)

