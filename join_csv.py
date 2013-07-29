#!/usr/bin/env python

from argparse import ArgumentParser
from csv import reader

parser = ArgumentParser()
parser.add_argument('--data', dest='paths', default=[], nargs='+', help='files to load')
parser.add_argument('--keys', nargs='+', type=int, help='which columns are keys')

def create_table(f, key_index):
    r = reader(f)
    data = {}
    for record in r:
        key = record[key_index]
        data[key] = record
    return data


def main():
    args = parser.parse_args()
    datas = {}
    for (path, key_index) in zip(args.paths, args.keys):
        with open(path, 'r') as f:
            datas[path] = create_table(f, key_index)
    work = zip(args.paths, args.keys)
    work.reverse()
    (accum_table, accum_key_index) = work.pop()
    accum = datas[accum_table].values()
    for (right_table, right_index) in work:
        right = datas[right_table]
        for record in accum:
            accum_key = record[accum_key_index]
            right_record = right[accum_key]
            before = right_record[:right_index]
            after = right_record[(right_index+1):]
            record.extend(before+after)
    for record in accum:
        print ", ".join(map(str,record))

if __name__ == '__main__':
    main()
