import sys
import json
from listed import get_item_iter
from words import get_normalized_words


def main():
    words_f = open(sys.argv[1], 'r')
    json_data = words_f.read()
    top_words = json.loads(json_data)
    items = get_item_iter(sys.argv[2])
    for item in items:
        item_words = set(get_normalized_words(item))
        item_vec = [str(item['id'])]
        for word in top_words:
            if word in item_words:
                item_vec.append("1")
            else:
                item_vec.append("0")
        print ", ".join(item_vec)

if __name__ == '__main__':
    main()

