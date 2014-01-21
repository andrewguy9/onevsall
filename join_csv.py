#!/usr/bin/env python

import argparse
from argparse import ArgumentParser
from csv import reader, writer
from sys import stdout
from tempfile import NamedTemporaryFile
from os import link

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

class table(object):

    def __init__(self, header):
        self.has_headers = header

    def get_iter(self):
        raise NotImplemented()

    def get_headers(self):
        if self.has_headers:
            i = self.get_iter()
            headers = i.next()
            return headers
        else:
            return None

    def cursor(self):
        i = self.get_iter()
        if self.has_headers:
            i.next()
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
            index[key] = list(record[0:key_index] + record[key_index+1:])
        return index

    def write(self, f):
        out = writer(f)
        for record in self.cursor():
            out.writerow(map(str, record))

class file_table(table):
    def __init__(self, path, has_headers=True):
        super(file_table, self).__init__(has_headers)
        self.path = path

    def get_iter(self):
        fd = open(self.path, 'r')
        r = reader(fd)
        return r

class list_table(table):
    table = []

    def __init__(self, input_, has_headers=True):
        super(list_table, self).__init__(has_headers)
        self.table = [list(x) for x in input_]

    def get_iter(self):
        return iter(self.table)

def merge_records(left, left_key, right_index):
    for record in left.cursor():
        key = record[left_key]
        right = right_index[key]
        try:
            yield record + right
        except TypeError as e:
            print record
            print right
            raise e

def left_join(left, left_key, right_index):
    combined = merge_records(left, left_key, right_index)
    table = list_table(combined)
    return table

def main():
    args = parser.parse_args()
    accum = file_table(args.base, False)  # TODO Does this table have headers?
    if args.output:
        out_h = NamedTemporaryFile()
    else:
        out_h = stdout
    # print "***Start table***"
    # accum.write(stdout)
    for (table_name, left_index, right_index) in args.join_arg:
        right = file_table(table_name, False)  # TODO Does this table have headers?
        # print "***right table ***"
        # right.write(stdout)
        index = right.index(right_index)
        accum = left_join(accum, left_index, index)
        # print "***joined table***"
        # accum.write(stdout)
    accum.write(out_h)
    if out_h != stdout:
        link(out_h.name, args.output)

if __name__ == '__main__':
    main()
