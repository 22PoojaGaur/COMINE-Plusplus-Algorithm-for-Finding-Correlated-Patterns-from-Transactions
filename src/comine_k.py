from globals import MIN_SUPPORT, MIN_ALL_CONF

def get_all_prefixes(suffixes, T):
    '''
    returns a 2d list of all prefixes for an item in tree T
    '''

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
    '''
    Returms max support allowed for this item.
    '''
    return max (counts[item] / MIN_ALL_CONF, MIN_SUPPORT)


def find_max_item_support(pattern, counts):
    '''
    Returns support of item with maximum support among items in pattern.

    pattern: List. list of items in pattern.
    counts: Dict. item -> count dict
    '''

    max_support = -1 

    for item in pattern:
        if counts[item] > max_support:
            max_support = counts[item]
    
    return max_support


def find_support(pattern, counts):
    '''
    This method considers support of a pattern as the minimum support among its items

    patterns: List. list of items in pattern.
    counts: Dict. dictionary of counts of items
    '''

    min_support = None
    for item in pattern:
        if min_support is None:
            min_support = counts[item]
        else:
            if counts[item] < min_support:
                min_support = counts[item]
    
    return min_support


def cominek(T, alpha, k):
    '''
    T: Object. Object of class Tree.
    alpha: List. alpha for alpha projected database.
    k: Int. Number of call made to this function. This is added because
        function acts differently when called 1st time vs when called
        subsequent times.
    '''

    # TODO: Implement header in the Tree structure
    for ai in T.header.keys():
        beta = set(alpha) + set(ai)

        all_conf = find_support (list(beta)) / max_item_support (list(beta), T.item_counts) # sup(beta) = sup()

        # get support range for ai
        support_limit = get_support_max_limit(ai, T.item_counts)
        all_prefixes = get_all_prefixes(T.header[ai], T)
        for prefix in all_prefixes:

            # check support condition for each item in prefix path
            check_passed = []
            for item in prefix:
                # the prefix contains ai as well
                if T.node_to_item[item] == ai:
                    continue

                if find_support([item]) <= support_limit:
                    check_passed.append(item)
                else:
                    break

            # create temporary branch with items in prefix that satisfy
            # the test, preserve the node counts of the items and their
            # orders in the temporary branch

            # add the temporary branch in the beta projected database
            
            pass

        # Ibeta = items in beta projected database
        Ibeta = []
        for bj in Ibeta:
            if find_suport (set(beta) + set(bj)) < minSup:
                # delete node

                pass
            if find_all_conf (set(beta) + set(bj)) < minAllConf:
                # delete node

                pass

        # construct beta conditional fp-tree with items in Ibeta Tbeta
        if Tbeta != NULL:
            cominek (Tbeta, beta)


if __name__ == '__main__':
    # Write code for testing here