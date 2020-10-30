from collections import OrderedDict

def get_frequent_item_count_dict(fin):
    item_count_dict = {}  
    # 2-d array to store data
    data = []
    for trans in fin.readlines():
        t = trans.strip().split(';')
        data.append(t)
    '''
    transaction -> a c b
    data_dict = {
        'a': 2,
        'b': 3,
        'c': 1
    }
    '''
    for trans in data:
        for item in trans:
            if item in item_count_dict:
                item_count_dict[item] += 1
            else:
                item_count_dict[item] = 1

    return (OrderedDict(sorted(item_count_dict.items(), key=lambda item:item[1], reverse=True)), data)
