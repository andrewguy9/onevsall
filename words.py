import argparse
from listed import get_item_iter, flatten
import re
from stemming.porter2 import stem
from itertools import imap

def get_words(item):
    item_words = item['title'].split() + item['description'].split()
    for word in item_words:
        yield word

def get_normalized_words(item):
    for word in get_words(item):
        try:
            word = normalize(word)
        except ValueError:
            pass
        else:
            yield word

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
    item_iters = []
    for f in args.files:
        item_iters.append(get_item_iter(f))
    items = flatten(item_iters)
    item_texts = imap(get_normalized_words, items)
    words = flatten(item_texts)
    counts = count(words)
    top_word_counts = counts[0:int(args.count)]
    top_words = map(lambda x: x[0], top_word_counts)
    for (idx, word) in zip(range(len(top_words)), top_words):
        print "%d,%s" % (idx, word)

parser = argparse.ArgumentParser()
parser.add_argument('count', type=int, help='number of words to track')
parser.add_argument('text_fields', help='indexes to extract from csv.')
parser.add_argument('files', nargs='*', help='file to parse')
if __name__ == '__main__':
    main()
