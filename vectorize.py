from join_csv import file_table
from listed import get_item_iter
from os import rename
from sys import stdout
from tempfile import NamedTemporaryFile
from words import get_words, normalize_words
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--output', help='Output file path')
parser.add_argument('words', help='list of words to use')
parser.add_argument('fields', help='items')
parser.add_argument('items', help='items')
def main():
    args = parser.parse_args()
    top_words = file_table(args.words)
    items = get_item_iter(args.items)
    if args.output:
        out_h = NamedTemporaryFile()
    else:
        out_h = stdout
    for item in items:
        item_words = get_words(args.fields.split(','), item)
        norm_item_words = list(normalize_words(item_words))
        item_vec = [str(item['id'])]
        for idx, word in top_words.cursor():
            if word in norm_item_words:
                item_vec.append("1")
            else:
                item_vec.append("0")
        print >>out_h, ",".join(item_vec)
    if out_h != stdout:
        rename(out_h.name, args.output)

if __name__ == '__main__':
    main()
