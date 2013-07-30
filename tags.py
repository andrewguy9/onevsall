from csv import reader
from listed import tail
import sys

def get_tags(path):
    f = open(path, 'r')
    r = reader(f)
    items = tail(r)
    tag_max = 0
    tags = {}
    for item in items:
        (title, tag, price, id) = item
        # print item
        try:
            tag_id = tags[tag]
        except KeyError:
            tag_id = tag_max
            tags[tag] = tag_id
            tag_max += 1
    return tags

def main():
    tags = get_tags(sys.argv[1])
    for tag, id in tags.items():
        print "%d,%s"%(id,tag)

if __name__ == '__main__':
    main()
