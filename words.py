import argparse
from listed import get_item_iter
from listutils import flatten
import re
from stemming.porter2 import stem
from itertools import imap
from tempfile import NamedTemporaryFile
from os import link
from sys import stdout

def get_item_words(item, fields, excluded):
    words = get_words(fields, item)
    normalized_words = normalize_words(words)
    filtered_words = filter_words(words, excluded_words)
    return filtered_words

re_flags = re.MULTILINE | re.DOTALL | re.UNICODE
word_regex = re.compile("([a-z]+)", re_flags)
def get_words(fields, item):
    for field in fields:
        data = item[field]
        words = word_regex.finditer(data)
        for word_match in words:
            word = word_match.groups()[0]
            yield word

def normalize_words(words):
    for word in words:
        try:
            yield normalize(word)
        except ValueError:
            pass

def filter_words(words, excluded):
    return [ i for i in words if i not in excluded ]

def ngrams(it, n):
    assert(n > 0)
    l = list(it)
    if len(l) < n:
        return []
    window = l[:n]
    grams = [tuple(window)]
    for i in l[n:]:
        window = window[1:]
        window.append(i)
        grams.append(tuple(window))
    return grams

def one2ngrams(it, n):
    l = list(it)
    all_grams = []
    for i in range(1, n+1):
        all_grams += ngrams(l, i)
    return all_grams

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

def accum(i, uniq):
    for item in i:
        try:
            uniq[item] += 1
        except KeyError:
            uniq[item] = 1

def reverse(t):
    (a, b) = t
    return (b, a)

def main():
    args = parser.parse_args()
    if args.exclude:
        with open(args.exclude, 'r') as f:
            excluded_words = set([w for w in f.read().split('\n')])
    else:
        excluded_words = set()
    fields = args.fields.split(',')
    counts = {}
    item_iters = [get_item_iter(f) for f in args.files]
    for item_iter in item_iters:
        for item in item_iter:
            words = get_item_words(item, fields, excluded)
            grams = one2ngrams(words, args.ngrams)
            accum(grams, counts)
    top_word_counts = [(count,word) for word, count in counts.items()]
    top_word_counts = sorted(top_word_counts, reverse=True)
    top_word_counts = top_word_counts[0:int(args.count)]
    top_words = map(lambda x: x[1], top_word_counts)
    if args.output:
        out_h = NamedTemporaryFile()
    else:
        out_h = stdout
    for idx, word in enumerate(top_words):
        print >>out_h, "%s,%s" % (idx, " ".join(list(word)))
    if out_h != stdout:
        link(out_h.name, args.output)


parser = argparse.ArgumentParser()
parser.add_argument('count', type=int, help='number of words to track')
parser.add_argument('fields', help='comma separated list of fields to extract.')
parser.add_argument('files', nargs='*', help='file to parse')
parser.add_argument('--exclude', help='file with list of stop words to exclude')
parser.add_argument('--output', help='output file path')
parser.add_argument('--ngrams', type=int, default=1, help="That ngrams to collect")
if __name__ == '__main__':
    main()
