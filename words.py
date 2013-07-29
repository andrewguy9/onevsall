from listed import *
import re
from stemming.porter2 import stem
import sys
import json
from listed import *

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
            uniq[item]+=1
        except KeyError:
            uniq[item]=1
    items = uniq.items()
    items = map(reverse, items)
    items = sorted(items)
    items = map(reverse, items)
    items.reverse()
    return items

def reverse(t):
    (a,b) = t
    return (b,a)

def main():
    item_iter = get_item_iter(sys.argv[1])
    items = [ i for i in item_iter]
    words = [ get_normalized_words(item) for item in items]
    words = flatten(words)
    counts = count(words)
    top_word_counts = counts[1:int(sys.argv[2])]
    top_words = map(lambda x: x[0], top_word_counts)
    json_data = json.dumps(top_words)
    print json_data

if __name__ == '__main__':
    main()

