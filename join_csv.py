#!/usr/bin/env python

import argparse
from argparse import ArgumentParser
from csv import reader, writer
from sys import stdout
from tempfile import NamedTemporaryFile
from os import rename

def join_arg(string):
    try:
        (table, left_key, right_key) = string.split(":")
        table = str(table)
        left_key = int(left_key)
        right_key = int(right_key)
    except Exception:
        raise argparse.ArgumentTypeError("format is file:left_key:right_key")
    else:
        return (table, left_key, right_key)

# fileA fileB keyA keyB fileC keyC keyD
parser = ArgumentParser()
parser.add_argument('--output', help='file to write to')
parser.add_argument("base", help="table to start with")
parser.add_argument("join_arg", type=join_arg, nargs='*', help="file.csv:left_key_index:right_key_index")

class table:
    def __init__(self, path):
        self.path = path

    def cursor(self):
        with open(self.path, 'r') as fd:
            r = reader(fd)
            for record in r:
                yield record

    def dict_cursor(self):
        with open(self.path, 'r') as fd:
            r = reader(fd)
            headers = r.next()
            index_field = list(enumerate(headers))
            for row in r:
                dict_row = {field: row[index] for (index, field) in index_field}
                yield dict_row

    def index(self, key_index):
        index = {}
        for record in self.cursor():
            key = record[key_index]
            if key in index:
                raise ValueError("Key %s is not unique" % key)
            index[key] = record
        return index

    def write(self, f):
        out = writer(f)
        for record in self.cursor():
            out.writerow(map(str, record))

def left_join(left, left_key, right_index, right_key):
    accum = []
    # print "&&& running key %d &&&" % left_key
    for record in left.cursor():
        row = []
        row += record
        key = record[left_key]
        # print "&&& For this record, '%s' is the key &&&" % key
        right_record = right_index[key]
        before = right_record[:right_key]
        after = right_record[(right_key+1):]
        row.extend(before+after)
        # print "==== This row is now ", row
        accum.extend([row])
    return accum

def main():
    args = parser.parse_args()
    accum = table(args.base)
    if args.output:
        out_h = NamedTemporaryFile()
    else:
        out_h = stdout
    # print "***Start table***"
    # accum.write(stdout)
    for (table_name, left_index, right_index) in args.join_arg:
        right = table(table_name)
        # print "***right table ***"
        # right.write(stdout)
        index = right.index(right_index)
        accum = left_join(accum, left_index, index, right_index)  # TODO FIX JOIN.
        # print "***joined table***"
        # accum.write(stdout)
    accum.write(stdout)
    if out_h != stdout:
        rename(out_h.name, args.output)

if __name__ == '__main__':
    main()
