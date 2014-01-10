#!/usr/bin/env python

import argparse
from argparse import ArgumentParser
from csv import reader, writer
from sys import stdout
from tempfile import NamedTemporaryFile
from os import rename
from listutils import flatten

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

    def get_iter(self):
        raise NotImplemented()

    def cursor(self):
        i = self.get_iter()
        for record in i:
            yield record

    def dict_cursor(self):
        i = self.get_iter()
        headers = i.next()
        index_field = list(enumerate(headers))
        for row in i:
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

class file_table(table):
    def __init__(self, path):
        self.path = path

    def get_iter(self):
        fd = open(self.path, 'r')
        r = reader(fd)
        return r

class list_table(table):
    table = []

    def __init__(self, input_):
        self.table = [tuple(x) for x in input_]

    def get_iter(self):
        return self.table

def merge_records(left, left_key, right_index):
    for record in left.cursor():
        key = record[left_key]
        right = right_index[key]
        yield flatten([record, right])

def left_join(left, left_key, right_index):
    combined = merge_records(left, left_key, right_index)
    table = list_table(combined)
    return table

def main():
    args = parser.parse_args()
    accum = file_table(args.base)
    if args.output:
        out_h = NamedTemporaryFile()
    else:
        out_h = stdout
    # print "***Start table***"
    # accum.write(stdout)
    for (table_name, left_index, right_index) in args.join_arg:
        right = file_table(table_name)
        # print "***right table ***"
        # right.write(stdout)
        index = right.index(right_index)
        accum = left_join(accum, left_index, index)
        # print "***joined table***"
        # accum.write(stdout)
    accum.write(out_h)
    if out_h != stdout:
        rename(out_h.name, args.output)

if __name__ == '__main__':
    main()
