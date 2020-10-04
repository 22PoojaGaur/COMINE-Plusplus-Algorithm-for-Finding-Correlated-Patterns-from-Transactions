import get_frequent_items
import sys

if __name__ == '__main__':
    fin = open(sys.argv[1], 'r')

    item_count_dict = get_frequent_items.get_frequent_item_count_dict(fin)
    print (item_count_dict)