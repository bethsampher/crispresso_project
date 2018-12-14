#!/usr/bin/python

import csv
import os
import re

#with open("/tmp/Miseq_049/Miseq_049.csv") as miseq:
   # miseq_reader = csv.reader(miseq)
    #for row in miseq_reader:
     #   print(row[0].rjust(20)),
      #  print(row[1].rjust(10)),
       # print(row[2].rjust(20)),
        #print(row[3].rjust(5))

fileregex = re.compile(r'^(\d+)_S\1_L001_R([1])_001\.fastq\.gz$')

with open("/tmp/Miseq_049/Miseq_049.csv") as miseq:
    miseq_reader = csv.DictReader(miseq)
    readlist = []
    for read in miseq_reader:
        readlist.append(read)
    for filename in os.listdir("/tmp/Miseq_049"):
        file_match = fileregex.search(filename)
        if file_match is None:
            continue
        filename_two = '{num}_S{num}_L001_R2_001.fastq.gz'.format(num = file_match.group(1))
        for dictionary in readlist:
            if int(file_match.group(1)) >= int(dictionary['min_index']) and int(file_match.group(1)) <= int(dictionary['max_index']):
                print(filename)
                print(filename_two)
                print(dictionary['Crispr']) 
                print(dictionary['Amplicon'])


                
            


