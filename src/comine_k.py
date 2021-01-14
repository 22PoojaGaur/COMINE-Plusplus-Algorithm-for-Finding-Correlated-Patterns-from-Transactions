from globals import MIN_SUPPORT, MIN_ALL_CONF
import pprint
from tree import Tree
import logging


def get_support_max_limit(item, counts):
    """
    Returms max support allowed for this item.
    """
    return int(max(counts[item] / MIN_ALL_CONF, MIN_SUPPORT))


def find_max_item_support(pattern, supports):
    """
    Returns support of item with maximum support among items in pattern.

    pattern: List. list of items in pattern.
    supports: Dict. item -> count dict
    """

    max_support = -1

    for item in pattern:
        max_support = max(max_support, supports[item])

    return max_support


def find_max_support_with_nc(pattern, sup_counts):

    max_support = -1
    for item in pattern:
        if sup_counts[item] > max_support:
            max_support = sup_counts[item]

    return max_support


def find_support(pattern, supports):
    """
    This method considers support of a pattern as the minimum support among its items

    patterns: List. list of items in pattern.
    supports: Dict
    """
    min_support = None

    for item in pattern:
        if min_support is None:
            min_support = supports[item]
        else:
            if supports[item] < min_support:
                min_support = supports[item]

    return min_support

def find_support_new(pattern, tree):
    min_support = None
    if len(pattern) == 1:
        # the support count is simply sum of all counts in header
        sup = 0
        for node in tree.header[pattern[0]]:
            sup += node.node_count

    else:
        idx = 0
        first = pattern[idx]
        current_node = tree.header[first][0]
        sup = current_node.node_count

        while idx < len(pattern)+1:
            next_node = pattern[idx+1]
            sup = min(sup)


    pass


def find_support_with_nc(pattern, sup_counts):
    min_support = None

    for item in pattern:
        if min_support is None:
            min_support = sup_counts[item]
        else:
            if sup_counts[item] < min_support:
                min_support = sup_counts[item]

    return min_support


def find_all_conf(pattern):
    pass


def get_prefixes(snodes):
    """
    snodes: List. List of suffix nodes for a header
    """
    all_prefixes = []
    for node in snodes:
        prefix = []
        count = node.node_count
        while node.parent is not None:
            prefix.append(tuple([node.item, count]))
            node = node.parent
        all_prefixes.append(prefix)

    return all_prefixes


def cominek(T, suffix=None, k=1, data=None, support_suffix=0):
    """
    T: Object. Object of class Tree.
    alpha: List. alpha for alpha projected database.
    k: Int. Number of call made to this function. This is added because
        function acts differently when called 1st time vs when called
        subsequent times.
    """
    if suffix is not None:
        logging.debug('Running cominek with suffix %s and k is %s ', ' '.join(suffix), str(k))
    else:
        logging.debug('Running cominek with empty suffix')

    logging.debug('Header for the tree passed is ')
    logging.debug(T.get_header_sorted())

    for ai, nc in T.get_header_sorted():
        logging.debug('Process for header item %s ', ai)

        if suffix is None:
            beta = [ai]
            support_beta = T.get_item_support(ai)
        else:
            beta = list(set(suffix).union(set(ai)))
            support_beta = min(support_suffix, T.get_item_support(ai))

        logging.debug('BETA is %s', ' '.join(beta))
        logging.debug('Support of beta is %s ', str(support_beta))

        if support_beta >= MIN_SUPPORT and support_beta / T.max_support(beta) >= MIN_ALL_CONF:
            print ("FINAL BETA ", ' '.join(beta))

        all_conf = support_beta / T.max_support(beta)
        logging.debug('All conf for beta is %s ', str(all_conf))

        # get support range for ai
        support_limit = max(T.get_item_support(ai) / MIN_ALL_CONF, MIN_SUPPORT)

        logging.debug('Support limit for beta is %s ', str(support_limit))
        all_prefixes = get_prefixes(T.header[ai])

        logging.debug('All prefixes for header element %s is ', ai)
        logging.debug(all_prefixes)

        beta_tree = Tree()

        for prefix in all_prefixes:

            # check support condition for each item in prefix path
            check_passed = []
            for item in prefix:
                # the prefix contains ai as well
                if item[0] == ai:
                    continue

                if T.get_item_support(item[0]) <= support_limit:
                    check_passed.append(item)
                else:
                    break

            # add the temporary branch in the beta projected database
            check_passed.reverse()
            print('\nTemp branch for prefix ', prefix)
            print(check_passed)

            if len(check_passed) > 0:
                logging.debug('Inserting %s in beta tree ', ' '.join([c[0] for c in check_passed]))
                beta_tree.insert_transaction([c[0] for c in check_passed], nc=check_passed[0][1])  # considering check passed has tuples

        beta_tree.merge_tree()

        logging.debug('Beta tree formed for %s is ', ' '.join(beta))
        logging.debug(beta_tree)

        beta_tree.print()

        for node in beta_tree.get_all_nodes():
            if node.item is None:
                continue
            pattern = list(set(beta).union(set(node.item)))
            pattern_support = min(support_beta, beta_tree.get_item_support(node.item))
            if pattern_support < MIN_SUPPORT:
                # delete this node
                beta_tree.delete_node(node)

            elif pattern_support / T.max_support(pattern) < MIN_ALL_CONF:
                # delete this node
                beta_tree.delete_node(node)
            else:
                print ('PATTERN HERE ', ' '.join(pattern))

        logging.debug('Final beta tree after node deletion is ')
        logging.debug(beta_tree)

        beta_tree.print()
        print(beta_tree.header)

        # call if more than one element in fp tree
        if beta_tree.count_nodes() > 1:
            cominek(beta_tree, beta, len(beta)+1, data=data, support_suffix=support_beta)


if __name__ == '__main__':
    # Write code for testing here
    pass
