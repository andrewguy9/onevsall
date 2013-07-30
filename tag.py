from csv import reader
from listed import tail
from tags import get_tags
import sys

def get_tags_iter(path, tags):
    f = open(path, 'r')
    r = reader(f)
    items = tail(r)
    for item in items:
        (title, tag, price, id) = item
        tag_id = tags[tag]
        vec = [ id, str(tag_id) ]
        yield vec

def main():
    tags = get_tags(sys.argv[1])
    for item in get_tags_iter(sys.argv[1], tags):
        print ",".join(item)

if __name__ == '__main__':
    main()
