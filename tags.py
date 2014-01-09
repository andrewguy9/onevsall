from sys import stdout
from os import rename
from tempfile import NamedTemporaryFile
import argparse
from join_csv import table

def get_tags(path):
    tags = set()
    for item in table(path).dict_cursor():
        tags.add(item['tag'])
    return sorted(tags)

parser = argparse.ArgumentParser()
parser.add_argument('--output', help='file to write to')
parser.add_argument('tagged_items', help='File to extract tags from')
def main():
    args = parser.parse_args()
    tagged_items = get_tags(args.tagged_items)
    if args.output:
        out_h = NamedTemporaryFile()
    else:
        out_h = stdout
    for id, tag in enumerate(tagged_items):
        print >>out_h, "%d,%s" % (id, tag)
    if out_h != stdout:
        rename(out_h.name, args.output)

if __name__ == '__main__':
    main()
