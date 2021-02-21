from collections import OrderedDict

import queue
import logging


class IdGenerator:
    """
    The ids have many to 1 relationship with the itemnames.
    """

    def __init__(self):
        self.id_count = 0
        self.id_to_node = {}

    def get_new_id(self, node):
        self.id_count += 1
        self.id_to_node[self.id_count] = node
        return self.id_count

    def get_node_for_id(self, id):
        try:
            return self.id_to_node[id]
        except KeyError:
            raise ValueError("This id is not valid, " + str(id))


class Node:

    def __init__(self, item_name=None, id=None, children=None, nc=1, id_gen=None):
        if children is None:
            children = {}
        self.children = children
        self.item = item_name
        if id_gen is not None:
            self.id = id_gen.get_new_id(self)
        else:
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
        self.id_generator = IdGenerator()  # id generator for this tree

    def get_header_sorted(self):
        # returns header sorted by item support counts
        it = sorted(self.header.items(), key=lambda v: sum([n.node_count for n in v[1]]), reverse=True)
        return it

    def get_item_support(self, item):
        sup = 0
        if item not in self.header:
            # raise ValueError("The item passed does not belong to this tree, " + str(item))
            return 0  # TODO: not sure why pass should work

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
                    raise ValueError("Suffix is not present in children. This should not happen, " + child.item)

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
                new_child = Node(trans[t], nc=nc, id_gen=self.id_generator)
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
            while cidx < len(sorted_level) - 1:
                if sorted_level[cidx].item != sorted_level[cidx + 1].item:
                    merged_level.append(sorted_level[cidx])
                    cidx += 1
                    continue
                else:
                    # modify header
                    self.header[sorted_level[cidx].item].remove(sorted_level[cidx])
                    self.header[sorted_level[cidx].item].remove(sorted_level[cidx + 1])

                    for child in sorted_level[cidx].children:
                        if child in sorted_level[cidx + 1].children:
                            sorted_level[cidx + 1].children[child].node_count += sorted_level[cidx].children[
                                child].node_count
                        else:
                            sorted_level[cidx + 1].children[child] = sorted_level[cidx].children[child]
                    # del prev_level.children[sorted_level[cidx].item]
                    sorted_level[cidx + 1].node_count += sorted_level[cidx].node_count

                    self.header[sorted_level[cidx + 1].item].append(sorted_level[cidx + 1])
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

        print('DEBUG: this parent')
        print(this_parent == self.root)
        print(this_parent.children)
        print(this_parent.item)

        if this_parent is None:
            pass
        else:
            # this is a hacky way to handle the case where children A - B C and children B - C, and we want to delete B.
            try:
                del this_parent.children[node.item]
            except KeyError:
                pass

        for n in node.children:
            node.children[n].parent = this_parent
            # this is a hacky way to handle the case where children A - B C and children B - C, and we want to delete B.
            if node.children[n].item not in this_parent.children:
                this_parent.children[node.children[n].item] = node.children[n]

    def count_nodes(self):
        return len(self.get_all_nodes())
