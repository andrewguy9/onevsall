#!/usr/bin/env python

import argparse
from argparse import ArgumentParser
from csv import reader

def join_arg(string):
    try:
        (table,left_key, right_key) = string.split(":")
        table = str(table)
        left_key = int(left_key)
        right_key = int(right_key)
    except Exception:
        raise argparse.ArgumentTypeError("format is file:left_key:right_key")
    else:
        return (table,left_key, right_key)

# fileA fileB keyA keyB fileC keyC keyD
parser = ArgumentParser()
parser.add_argument("base", help="table to start with")
parser.add_argument("join_arg", type=join_arg, nargs='+', help="file.csv:left_key_index:right_key_index")

def create_table(f):
    r = reader(f)
    table = []
    for record in r:
        table.append(record)
    return table

def create_table_with_index(f, key_index):
    table = create_table(f)
    index = {}
    for record in table:
        key = record[key_index]
        index[key] = record
    return index


def main():
    args = parser.parse_args()
    with open(args.base, 'r') as accum_f:
        accum = create_table(accum_f)
    for (table_name,left_index,right_index) in args.join_arg:
        with open(table_name, 'r') as f:
            table = create_table_with_index(f, right_index)
            for record in accum:
                accum_key = record[left_index]
                right_record = table[accum_key]
                before = right_record[:right_index]
                after = right_record[(right_index+1):]
                record.extend(before+after)
    for record in accum:
        print ", ".join(map(str,record))

if __name__ == '__main__':
    main()
