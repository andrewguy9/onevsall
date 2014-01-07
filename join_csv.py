#!/usr/bin/env python

import argparse
from argparse import ArgumentParser
from csv import reader, writer
from sys import stdout

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
parser.add_argument("base", help="table to start with")
parser.add_argument("join_arg", type=join_arg, nargs='*', help="file.csv:left_key_index:right_key_index")

def create_table(f):
    r = reader(f)
    table = []
    for record in r:
        table.append(record)
    return table

def create_index(table, key_index):
    index = {}
    for record in table:
        key = record[key_index]
        if key in index:
            raise ValueError("Key %s is not unique" % key)
        index[key] = record
    return index

def left_join(left, left_key, right_index, right_key):
    accum = []
    # print "&&& running key %d &&&" % left_key
    for record in left:
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

def print_table(table, f):
    out = writer(f)
    # print table
    for record in table:
        # print record
        out.writerow(map(str, record))

def main():
    args = parser.parse_args()
    with open(args.base, 'r') as accum_f:
        accum = create_table(accum_f)
    # print "***Start table***"
    # print_table(accum, stdout)
    for (table_name, left_index, right_index) in args.join_arg:
        with open(table_name, 'r') as f:
            table = create_table(f)
            # print "***right table table***"
            # print_table(table, stdout)
            index = create_index(table, right_index)
            accum = left_join(accum, left_index, index, right_index)
            # print "***joined table***"
            # print_table(accum, stdout)
    print_table(accum, stdout)

if __name__ == '__main__':
    main()
