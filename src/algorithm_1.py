import get_frequent_items
import sys
from collections import OrderedDict
import copy
import pprint


class Tree:

    T = {}

    node_to_item = {}

    def __init__(self):
        self.T[0] = ([], 0)
        self.node_to_item = {}
        self.node_gen_count = 0

    def contains(self, item, node_ids):
        for node in node_ids:
            if self.node_to_item[node] == item:
                return (True, node)
        return (False, None)

    def insert_tree(self, p, P, parent):
        '''
        p: item to insert
        P: remaining list of items in transaction
        tree: tree
        parent: node to insert item on
        '''
        # print ('inserting ', p)

        self.T[parent] = (self.T[parent][0], self.T[parent][1]+1)

        (contains, idx) = self.contains(p, self.T[parent][0])
        if contains:
            # print (self.T)
            # p belongs to children of child
            if len(P) != 0:
                self.insert_tree(P[0], P[1:], idx)
            else:
                self.T[idx] = (self.T[idx][0], self.T[idx][1]+1)
        else:
            # get id for a new node i.e self.node_gen_count + 1
            self.node_gen_count += 1
            self.T[parent][0].append(self.node_gen_count)
            self.node_to_item[self.node_gen_count] = p
            self.T[self.node_gen_count] = ([], 0)

            # print (self.T)

            if len(P) != 0:
                self.insert_tree(P[0], P[1:], self.node_gen_count)
            else:
                self.T[self.node_gen_count] = (self.T[self.node_gen_count][0], self.T[self.node_gen_count][1] + 1)


def sort_transaction(trans, item_count_dict):
    '''
    trans: (list) transaction.
    item_count_dict: (dict) dictionary containing item vs support for item.
    '''
    trans_dict = {}

    for item in trans:
        trans_dict[item] = item_count_dict[item]

    trans_dict = OrderedDict(
        sorted(trans_dict.items(), key=lambda val: val[1], reverse=True))

    return list(trans_dict.keys())


if __name__ == '__main__':
    fin = open(sys.argv[1], 'r')

    (item_count_dict, data) = get_frequent_items.get_frequent_item_count_dict(fin)

    T = Tree()
    sorted_frequent_item = []
    # Root
    for trans in data:
        sorted_trans = sort_transaction(trans, item_count_dict)
        # print (sorted_trans)
        T.insert_tree(sorted_trans[0], sorted_trans[1:], 0)
        # print ('\n')

    pprint.pprint(T.T)

    print ('\n\n')
    pprint.pprint (T.node_to_item)

