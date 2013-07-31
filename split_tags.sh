#!/usr/bin/env bash

input=$1
output_a=$2
output_b=$3
percent=$4

input_lines=$(wc -l $input | awk '{print $1}')
lines_a=$(perl -e "print int($input_lines * $percent / 100)")
lines_b=$(perl -e "print $input_lines - $lines_a")

head -$lines_a $input > $output_a
tail -$lines_b $input > $output_b


