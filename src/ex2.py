# ex2.py
# Written by Anthony L. Leotta
# Description : open the stats.csv and create a summary of total file size by fileextension

import os
import csv
import sys
import time

input_filename = "stats.csv"
output_filename = "summary.csv"


try:
    input = open(input_filename, 'rb')
    stats_file = csv.reader(input, delimiter=',', quoting=csv.QUOTE_MINIMAL)
except IOError:
    print "Could not open input file:", input_filename
    sys.exit(-1)

try:
    output = open(output_filename, 'wb')
    summary_file = csv.writer(output, delimiter=',', quoting=csv.QUOTE_MINIMAL)

    # define a list of column names
    columns = ['ext', 'size', 'count']

    # write the column headers to the CSV
    summary_file.writerow(columns)  # write the header  to CSV file
except IOError:
    print "Could not open output file:", output_filename
    sys.exit(-1)

ext_stats={} # a dictionary to hold file extension sizes and counts as a tuple

total_rows = 0

#skip first row of the input file because it contains the column names

stats_file.next()

# stats_file
for row in stats_file:
    total_rows += 1
    #print row
    (path, filename, ext, size ) = row

    size = int(size) # must convert the size fronm string to an integer

    if ext not in ext_stats:
        ext_stats[ext] = (size,1)
    else:
        (ext_size, ext_count) = ext_stats[ext]
        ext_stats[ext] = (ext_size + size, ext_count + 1)

print "rows read ", total_rows

# sort extensions
extensions = sorted(ext_stats.keys())

for ext in extensions:
    (ext_size, ext_count) = ext_stats[ext]
    summary_file.writerow( [ext, ext_size, ext_count] )

print "rows read ", total_rows

input.close()
output.close()

print 'done'