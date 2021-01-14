from collections import OrderedDict


def get_frequent_item_count_dict(fin):
    item_count_dict = {}
    # 2-d array to store data
    data = []
    for trans in fin.readlines():
        t = trans.strip().split(';')
        data.append(t)
    """
    transaction -> a c b
    data_dict = {
        'a': 2,
        'b': 3,
        'c': 1
    }
    """
    # find support
    for trans in data:
        for item in trans:
            if item in item_count_dict:
                item_count_dict[item] += 1
            else:
                item_count_dict[item] = 1

    sorted_item_tuples = sorted(item_count_dict.items(), key=lambda item: item[1], reverse=True)
    result_dict = OrderedDict() # dictionary with key: item_name, value: count. Sorted by count
    for (item, count) in sorted_item_tuples:
        result_dict[item] = count

    return result_dict, data
