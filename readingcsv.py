#!/usr/bin/python

import csv

#with open("/tmp/Miseq_049/Miseq_049.csv") as miseq:
   # miseq_reader = csv.reader(miseq)
    #for row in miseq_reader:
     #   print(row[0].rjust(20)),
      #  print(row[1].rjust(10)),
       # print(row[2].rjust(20)),
        #print(row[3].rjust(5))


with open("/tmp/Miseq_049/Miseq_049.csv") as miseq:
    miseq_reader = csv.DictReader(miseq)
    readlist = []
    for read in miseq_reader:
        readlist.append(read)
    for dictionary in readlist:
        for x in range(0, 200):
            if x >= dictionary['min_index'] and x <= dictionary['max_index']:
               # print(str(x))
