#!/usr/bin/python

import csv
import os
import re
import subprocess
import os.path
import sys
import time

fileregex = re.compile(r'^(\d+)_S\1_L001_R([1])_001\.fastq\.gz$')
if len(sys.argv) < 2:
    print('Please also type the path of the csv file in the folder.')
    exit()
csv_name = sys.argv[1]
folder = os.path.dirname(csv_name)

class Crispresso():
    def __init__(self, experiment, barcode, parameters):
        self.output = open(experiment + '_' + str(barcode) + '.out', 'w')
        self.error = open(experiment + '_' + str(barcode) + '.err', 'w')
        self.process = (subprocess.Popen(parameters, stderr=self.error, stdout=self.output))
    def wait_close(self):
        self.process.wait()
        self.output.close()
        self.error.close()

def run_crispresso():
    counter = 0
    processes = []
    with open(os.path.join(folder, csv_name)) as spreadsheet:
        spreadsheet_reader = csv.DictReader(spreadsheet)
        readlist = []
        for read in spreadsheet_reader:
            readlist.append(read)
        for filename in os.listdir(folder):
            file_match = fileregex.search(filename)
            if file_match is None:
                continue
            barcode = int(file_match.group(1))
            filename_two = '{num}_S{num}_L001_R2_001.fastq.gz'.format(num = barcode)
            for dictionary in readlist:
                parameters = ['/usr/local/bin/CRISPResso', \
                        '-r1', os.path.join(folder, filename),\
                        '-r2', os.path.join(folder, filename_two),\
                        '-a',  dictionary['Amplicon'],\
                        '-g', dictionary['Crispr'],\
                        '-w', '50',\
                        '-o', 'S' + str(barcode) + 'exp' + dictionary['Experiment'],\
                        '--hide_mutations_outside_window_NHEJ']
                if dictionary['HDR'] is not '':
                    parameters.extend(['-e', dictionary['HDR']])
                if barcode >= int(dictionary['min_index']) and barcode <= int(dictionary['max_index']):
                    processes.append(Crispresso(dictionary['Experiment'], barcode, parameters))
                    counter += 1
                if counter >= 5:
                    return processes
                       


start_time = time.time()
processes = run_crispresso()
for process in processes:
    process.wait_close()
end_time = time.time()
print(str(end_time - start_time))
