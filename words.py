import argparse
from listed import get_item_iter, flatten
import re
from stemming.porter2 import stem
from itertools import imap

def get_words(fields, item):
    for field in fields:
        words = item[field].split()
        for word in words:
            yield word

def normalize_words(words):
    for word in words:
        try:
            yield normalize(word)
        except ValueError:
            pass

strip_punct = re.compile("^[a-z]+")
def normalize(word):
    word = word.lower()
    match = strip_punct.match(word)
    if match:
        word = match.group()
    else:
        raise ValueError(word)
    word = stem(word)
    return word

def count(i):
    uniq = {}
    for item in i:
        try:
            uniq[item] += 1
        except KeyError:
            uniq[item] = 1
    items = uniq.items()
    items = map(reverse, items)
    items = sorted(items)
    items = map(reverse, items)
    items.reverse()
    return items

def reverse(t):
    (a, b) = t
    return (b, a)

def main():
    args = parser.parse_args()
    fields = args.fields.split(',')
    item_iters = [get_item_iter(f) for f in args.files]
    items = flatten(item_iters)
    items_words = imap(lambda item: get_words(fields, item), items)
    words = flatten(items_words)
    normalized_words = normalize_words(words)
    counts = count(normalized_words)
    top_word_counts = counts[0:int(args.count)]
    top_words = map(lambda x: x[0], top_word_counts)
    for (idx, word) in zip(range(len(top_words)), top_words):
        print "%d,%s" % (idx, word)

parser = argparse.ArgumentParser()
parser.add_argument('count', type=int, help='number of words to track')
parser.add_argument('fields', help='comma separated list of fields to extract.')
parser.add_argument('files', nargs='*', help='file to parse')
if __name__ == '__main__':
    main()
