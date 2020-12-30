from globals import MIN_SUPPORT, MIN_ALL_CONF
import pprint
from tree import Tree


def get_all_prefixes(suffixes, T):
    """
    returns a 2d list of all prefixes for an item in tree T
    """

    all_prefixes = []
    for item in suffixes:
        prefix = []
        temp_item = item

        # this will add all items in prefix in reverse order to the 
        # prefix array except root
        while temp_item in T.parents.keys():
            prefix.append(temp_item)
            temp_item = T.parents[temp_item]

        all_prefixes.append(prefix)

    return all_prefixes


def get_support_max_limit(item, counts):
    """
    Returms max support allowed for this item.
    """
    return max(counts[item] / MIN_ALL_CONF, MIN_SUPPORT)


def find_max_item_support(pattern, T):
    """
    Returns support of item with maximum support among items in pattern.

    pattern: List. list of items in pattern.
    counts: Dict. item -> count dict
    """

    max_support = -1

    for item in pattern:
        if T.item_counts[item] > max_support:
            max_support = T.item_counts[item]

    return max_support


def find_max_support_with_nc(pattern, sup_counts):

    max_support = -1
    for item in pattern:
        if sup_counts[item] > max_support:
            max_support = sup_counts[item]

    return max_support


def find_support(pattern, T):
    """
    This method considers support of a pattern as the minimum support among its items

    patterns: List. list of items in pattern.
    T: Object. Tree object.
    """
    # print('T.item_counts')
    # print(T.node_to_item)

    min_support = None

    for node_id in pattern:
        item = node_id
        if min_support is None:
            min_support = T.item_counts[item]
        else:
            if T.item_counts[item] < min_support:
                min_support = T.item_counts[item]

    return min_support


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


def cominek(T, alpha, k):
    """
    T: Object. Object of class Tree.
    alpha: List. alpha for alpha projected database.
    k: Int. Number of call made to this function. This is added because
        function acts differently when called 1st time vs when called
        subsequent times.
    """

    for ai in T.header.keys():
        print('\n\n Running for header key ', ai)
        if alpha is None:
            beta = set(ai)
        else:
            beta = set(alpha).union(set(ai))

        all_conf = find_support(list(beta), T) / find_max_item_support(list(beta), T)  # sup(beta) = sup()

        # get support range for ai
        support_limit = get_support_max_limit(ai, T.item_counts)
        all_prefixes = get_all_prefixes(T.header[ai], T)
        # print('\n all prefixes for ', ai)
        # pprint.pprint(all_prefixes)

        # temp_tree = Tree()
        # temp_tree.item_counts = T.item_counts
        # for k in T.header.keys():
        #     temp_tree.header[k] = []

        beta_tree = Tree()

        # Ibeta = list of items in beta projected database
        Ibeta = {}  # key = item, value = node_count
        # print ('\n initialized beta tree')
        # print (beta_tree.T)

        for prefix in all_prefixes:

            # check support condition for each item in prefix path
            check_passed = []
            for node_id in prefix:
                # the prefix contains ai as well
                if T.node_to_item[node_id] == ai:
                    continue

                if find_support(T.node_to_item[node_id], T) <= support_limit:
                    check_passed.append(tuple([T.node_to_item[node_id], T.T[node_id][1]]))
                else:
                    break

            # create temporary branch with items in prefix that satisfy
            # the test, preserve the node counts of the items and their
            # orders in the temporary branch

            # add the temporary branch in the beta projected database
            check_passed.reverse()
            print('\nTemp branch for prefix ', prefix)
            print(check_passed)
            # print (check_passed)
            # # convert check_passed node_ids to patterns
            # check_passed = list(map(lambda x: T.node_to_item[x], check_passed))
            if len(check_passed) > 0:
                # temp_tree.insert_tree(check_passed[0], check_passed[1:], 0)
                beta_tree.insert_branch(check_passed)

                for item, node_count in check_passed:
                    if item in Ibeta.keys():
                        Ibeta[item] += node_count
                    else:
                        Ibeta[item] = node_count

        print('Beta tree for prefixes of header ', ai)
        pprint.pprint(beta_tree.T)
        #
        print ('node to item map for beta tree')
        pprint.pprint(beta_tree.node_to_item)
        pprint.pprint(beta_tree.item_to_node)

        it = Ibeta.keys()
        for bj in it:
            print('Bj is ->')
            print(bj)
            print('Beta ->')
            print(beta)
            sup_counts = {}
            for item in beta:
                sup_counts[item] = T.item_counts[item]

            sup_counts[bj] = Ibeta[bj]

            if find_support_with_nc(set(beta).union(set(bj)), sup_counts) < MIN_SUPPORT:
                del Ibeta[bj]
            if find_support_with_nc(set(beta).union(set(bj)), sup_counts) / find_max_support_with_nc(set(beta).union(set(bj)), sup_counts) < MIN_ALL_CONF:
                del Ibeta[bj]

        # construct beta conditional fp-tree with items in Ibeta Tbeta
        if len(Ibeta.keys()) > 0:
            cominek (beta_tree, beta, 2)


if __name__ == '__main__':
    # Write code for testing here
    pass
