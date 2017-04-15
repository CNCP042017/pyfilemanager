# ex1.py
# Written by Anthony L. Leotta
# Description : command line tool that will walk c:\ on Windows.
# starting path: c:\  so this won't work on Linux or Mac yet
# This program will produce a CSV file on every file that is on the C: drive.
# In the next excercise, this file will be used to create some summary statistics
# and then plot some pretty graphs using matplotlib and numpy.

import os
import csv
import sys
import time

top_path = "c:\\"

output_filename = "stats.csv"

# open a file handle
try:
    csvfile = open(output_filename, 'wb')
except IOError:
    print "Could not open file:", output_filename
    sys.exit(-1)

# tell the CSV library that the file will be used to write CSV
stats_file = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)

# define a list of column names
columns=['path', 'filename', 'ext', 'size']

# write the column headers to the CSV
stats_file.writerow(columns)  #write the header  to CSV file

rows=[] #list to keep track of all the files. This will be used as a temp buffer to speed upoI/O

count=0
buffer_size=10000
total_elapsed = 0

start = time.time()
for root, dirs, files in os.walk(top_path): #walk the directory structure
    for name in files:
        filename = os.path.join(root,name)
        parts = name.split('.')

        # a filename could have more than one period, in which case finding
        # the real extension using a period is problematic

        if len(parts)>1:
            ext = parts[len(parts)-1]
            base = '.'.join(parts[0:len(parts)-1])
        else:
            base = name
            ext = ''

        try:
            info = os.stat(filename) # get the file stats
            filesize = info.st_size
        except WindowsError:
            filesize = -1

        rows.append([root, name, ext.lower(), filesize])
        if count % 10000 == 0 :
            done = time.time()
            elapsed = done - start
            total_elapsed += elapsed
            start = time.time()
            if count>0:
                print 'found %d files in %.1f seconds, total elapsed %.1f seconds, total files %d'%(buffer_size,elapsed,total_elapsed,count)
            stats_file.writerows(rows)  # write out a chuck of rows, I/O will be faster this way,
            rows = []

        count+=1

if len(rows):
    done = time.time()
    elapsed = done - start
    total_elapsed += elapsed
    print 'found %d files in %f seconds, total elapsed %f' % (buffer_size, elapsed, total_elapsed)
    stats_file.writerows(rows)  # write out a chuck of rows, I/O will be faster this way,

csvfile.close() #close the file handle

print 'done'