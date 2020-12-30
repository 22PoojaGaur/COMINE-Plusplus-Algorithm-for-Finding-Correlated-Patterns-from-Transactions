from collections import OrderedDict


class Tree:
    # T = {}

    # header = OrderedDict()

    # this dict would store the parent node id for each node id. 
    # It is one to one mapping and works as the structure is a Tree i.e
    # each node has at most one parent.
    # parents = {}
    #
    # item_counts = {}
    #
    # node_to_item = {}
    #
    # item_to_node = {}

    def __init__(self):
        self.T = {0: ([], 0)}
        self.header = OrderedDict()
        self.node_to_item = {}
        self.item_to_node = {}
        self.node_gen_count = 0
        self.item_counts = {}
        self.parents = {}

    def contains(self, item, node_ids):
        for node in node_ids:
            if self.node_to_item[node] == item:
                return True, node
        return False, None

    def insert_tree(self, p, P, parent):
        """
        p: item to insert
        P: remaining list of items in transaction
        tree: tree
        parent: node to insert item on
        """
        # print ('inserting ', p)

        # self.T[parent] = (self.T[parent][0], self.T[parent][1] + 1)

        (contains, idx) = self.contains(p, self.T[parent][0])
        if contains:
            self.T[idx] = (self.T[idx][0], self.T[idx][1] + 1)

            if len(P) != 0:
                self.insert_tree(P[0], P[1:], idx)

            # # print (self.T)
            # # p belongs to children of child
            # if len(P) != 0:
            #     self.insert_tree(P[0], P[1:], idx)
            # else:
            #     self.T[idx] = (self.T[idx][0], self.T[idx][1] + 1)
        else:
            # get id for a new node i.e self.node_gen_count + 1
            self.node_gen_count += 1
            self.T[parent][0].append(self.node_gen_count)
            self.node_to_item[self.node_gen_count] = p
            self.T[self.node_gen_count] = ([], 1)
            # if we are inserting a new node, add it to header
            self.header[p].append(self.node_gen_count)

            # add entry for the parent
            self.parents[self.node_gen_count] = parent

            # print (self.T)
            if len(P) != 0:
                self.insert_tree(P[0], P[1:], self.node_gen_count)

            # if len(P) != 0:
            #     self.insert_tree(P[0], P[1:], self.node_gen_count)
            # else:
            #     self.T[self.node_gen_count] = (self.T[self.node_gen_count][0], self.T[self.node_gen_count][1] + 1)

    def insert_branch(self, node_tuples):
        print ('NODE TUPLES')
        print (node_tuples)
        # start from root
        current_level = 0
        node_gen_count = 1
        for node_name, node_count in node_tuples:

            if node_name in self.item_to_node.keys():
                pass
            else:
                self.item_to_node[node_name] = node_gen_count
                self.node_to_item[node_gen_count] = node_name
                node_gen_count += 1

            (contains, idx) = self.contains(self.item_to_node[node_name], self.T[current_level][0])

            if contains:
                self.T[idx] = (self.T[idx][0], self.T[idx][1] + node_count)

                current_level = idx
            else:
                self.T[current_level][0].append(self.item_to_node[node_name])
                self.T[self.item_to_node[node_name]] = ([], node_count)
