import argparse
from listed import get_item_iter
from listutils import flatten
import re
from stemming.porter2 import stem
from itertools import imap
from tempfile import NamedTemporaryFile
from os import link
from sys import stdout

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
    if args.exclude:
        with open(args.exclude, 'r') as f:
            exclude = set([w for w in f.read().split('\n')])
            filtered_counts = filter(lambda w: w[0] not in exclude, counts)
    else:
        filtered_counts = counts
    top_word_counts = filtered_counts[0:int(args.count)]
    top_words = map(lambda x: x[0], top_word_counts)
    if args.output:
        out_h = NamedTemporaryFile()
    else:
        out_h = stdout
    for (idx, word) in zip(range(len(top_words)), top_words):
        print >>out_h, "%s,%s" % (idx, word)
    if out_h != stdout:
        link(out_h.name, args.output)


parser = argparse.ArgumentParser()
parser.add_argument('count', type=int, help='number of words to track')
parser.add_argument('fields', help='comma separated list of fields to extract.')
parser.add_argument('files', nargs='*', help='file to parse')
parser.add_argument('--exclude', help='file with list of stop words to exclude')
parser.add_argument('--output', help='output file path')
if __name__ == '__main__':
    main()
