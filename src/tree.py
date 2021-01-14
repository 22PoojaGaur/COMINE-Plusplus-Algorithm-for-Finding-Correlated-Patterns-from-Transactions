from collections import OrderedDict

import queue
import logging


class Node:

    def __init__(self, item_name=None, id=None, children=None, nc=1):
        if children is None:
            children = {}
        self.children = children
        self.item = item_name
        self.id = id
        self.parent = None
        self.node_count = nc

    def add_child(self, node):
        """
        Add child `node` to the current node
        """
        self.children[node.item] = node
        node.parent = self


class Tree:

    def __init__(self):
        self.root = Node()  # root node

        self.header = {}  # list of nodes where each branch of that item starts, key=item_name, value=list of nodes

        self.T = {0: ([], 0)}
        # self.header = OrderedDict()
        self.node_to_item = {}
        self.item_to_node = {}
        self.node_gen_count = 0
        self.item_counts = {}
        self.parents = {}

    def get_header_sorted(self):
        # returns header sorted by item support counts
        it = sorted(self.header.items(), key=lambda v: sum([n.node_count for n in v[1]]), reverse=True)
        #logging.debug(it)
        return it

    def get_item_support(self, item):
        sup = 0
        if item not in self.header:
            return 0
        for node in self.header[item]:
            sup += node.node_count
        return sup

    def get_support(self, item, suffix):
        total_support = 0
        for node in self.header[item]:
            current = self.find_node_in_children(node, suffix[0])
            if current is None:
                continue
            cur_support = min(node.node_count, current.node_count)

            for nj in suffix[1:]:
                for child in current.children:
                    if nj == child:
                        current = current.children[child]
                        cur_support = min(cur_support, current.node_count)
                else:
                    logging.error('This state is not considered, suffix not present in children')
                    return -1

            total_support += cur_support

        return total_support

    def max_support(self, pattern):
        max_support = -1
        for item in pattern:
            max_support = max(max_support, self.get_item_support(item))
        return max_support

    def find_node_in_children(self, node, item):
        if node.item == item:
            return node
        if len(node.children) == 0:
            return None
        for n in node.children:
            result = self.find_node_in_children(node.children[n], item)

        if result is None:
            return result
        return None

    def insert_transaction(self, trans, nc=1):
        current = self.root
        for t in range(len(trans)):
            if trans[t] not in current.children:
                new_child = Node(trans[t], nc=nc)
                current.add_child(new_child)
                if trans[t] in self.header:
                    self.header[trans[t]].append(new_child)
                else:
                    self.header[trans[t]] = [new_child]
                current = new_child

            else:
                current = current.children[trans[t]]
                current.node_count += nc

    def merge_tree(self):
        new_level = []
        for node in self.root.children:
            new_level.append(self.root.children[node])

        prev_level = self.root
        while len(new_level) > 0:
            # apply merge at this level
            sorted_level = sorted(new_level, key=lambda k: k.item)
            cidx = 0
            merged_level = []
            while cidx < len(sorted_level)-1:
                if sorted_level[cidx].item != sorted_level[cidx+1].item:
                    merged_level.append(sorted_level[cidx])
                    cidx += 1
                    continue
                else:
                    # modify header
                    self.header[sorted_level[cidx].item].remove(sorted_level[cidx])
                    self.header[sorted_level[cidx].item].remove(sorted_level[cidx+1])

                    for child in sorted_level[cidx].children:
                        if child in sorted_level[cidx+1].children:
                            sorted_level[cidx+1].children[child] += sorted_level[cidx].children[child]
                        else:
                            sorted_level[cidx+1].children[child] = sorted_level[cidx].children[child]
                    del prev_level.children[sorted_level[cidx].item]
                    sorted_level[cidx + 1].node_count += sorted_level[cidx].node_count
                    self.header[sorted_level[cidx+1].item].append(sorted_level[cidx + 1])
                    cidx += 1
            new_level = []
            for node in merged_level:
                for sn in node.children:
                    new_level.append(node.children[sn])

    def print(self):
        q = queue.Queue()
        q.put(self.root)
        while not q.empty():
            node = q.get()
            # print(node)
            if node.item is not None:
                print(node.item + ' : ' + ' '.join(node.children))
            for n in node.children:
                q.put(node.children[n])

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
        print('NODE TUPLES')
        print(node_tuples)
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

    def get_all_nodes(self):
        result = []

        q = queue.Queue()
        q.put(self.root)

        while not q.empty():
            node = q.get()
            result.append(node)

            for n in node.children:
                q.put(node.children[n])
        return result

    def delete_node(self, node):
        this_parent = node.parent

        if this_parent is None:
            pass
        else:
            del this_parent.children[node.item]

        for n in node.children:
            node.children[n].parent = this_parent
            this_parent.children[node.children[n].item] = node.children[n]

    def count_nodes(self):
        return len(self.get_all_nodes())
