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

def create_table(f, key_index):
    r = reader(f)
    data = {}
    for record in r:
        key = record[key_index]
        data[key] = record
    return data


def main():
    args = parser.parse_args()
    with open(args.base, 'r') as accum_f:
        accum = create_table(accum_f, 0).values()
    for (table_name,left_index,right_index) in args.join_arg:
        with open(table_name, 'r') as f:
            table = create_table(f, right_index)
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
