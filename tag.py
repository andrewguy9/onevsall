from sys import stdout
from os import rename
from tempfile import NamedTemporaryFile
from tags import get_tags
import argparse
from join_csv import file_table

def get_tags_iter(path, tags):
    for item in file_table(path).dict_cursor():
        tag = item['tag']
        tag_id = tags[tag]
        vec = [item['id'], str(tag_id)]
        yield vec

parser = argparse.ArgumentParser()
parser.add_argument('--output', help='file to write to')
parser.add_argument('tags', help='File we read tags from')
def main():
    args = parser.parse_args()
    tags = get_tags(args.tags)
    tags_dict = dict(map(lambda x: tuple(reversed(x)), enumerate(tags)))
    if args.output:
        out_h = NamedTemporaryFile()
    else:
        out_h = stdout
    for item in get_tags_iter(args.tags, tags_dict):
        print >>out_h, ",".join(item)
    if out_h != stdout:
        rename(out_h.name, args.output)

if __name__ == '__main__':
    main()
