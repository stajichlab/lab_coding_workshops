#!/usr/bin/env python3

import argparse
import csv
import gzip
import re

from pathlib import Path

# Parser, provide -i and -o options for input and output.
parser = argparse.ArgumentParser(
    prog = 'make_manifest_from_fastq',
    description = 'Make a tsv metadata based on the names of files in the folder.'
    )

parser.add_argument('-i', '--indir', type=Path, help='Folder with fastq files')
parser.add_argument('-o', '--outtsv', type=Path, help='Tsv output')

args = parser.parse_args()

# :ist all files in the folder.
files = Path(args.indir).glob('*')

# Create an dictionary to hold the entries.
entries = dict()

for file in files:
    # Find the sample ID (A, B, C, D, etc.)
    # Match upper or lowercase of "s", then "amp".
    # Match "l" zero or one time, match "e" zero or one time, match "_" zero or one time.
    # Match upper or lowercase of "a-z" one time, and set the match as the capturing group by the parentheses.
    ID = re.findall(r'[Ss]ampl?e?_?([A-Za-z])', str(file))[0]
    
    # Match "R" or "pair" and set it the first capturing group.
    # Match any number (\d) and set it the second capturing group.
    # Use [1] to extract the second capturing group, which indicates R1 or R2.
    read = re.findall(r'(R|pair)(\d)+', str(file))[0][1]
    
    # Extract the file extension.
    ext = file.suffix
    
    # If the file extension is '.gz', use gzip.open(). Else use regular open().
    if ext == '.gz':
        fh = gzip.open(file)
    else:
        fh = open(file)
    
    # Read the file to get the line count.
    read_count = 0
    for line in fh:
        # Remove the newline (\n) character.
        line = line.strip()
        # Remove the empty line.
        if line:
            read_count += 1
    fh.close()
    
    # Since a single read contains 4 lines, devide the line count by 4 to get the read count.
    read_count = read_count / 4
    
    # Create an entry by the sample ID if it is not found in the dictionary.
    if ID not in entries:
        # Fill the first item [0 in index] with sample ID, leave the rest for read_1, read_2, read_1_count and read_2_count.
        entries[ID] = [ID, "", "", "", ""]
    
    # Fill read 1 in index 1 (which is the second item) or read 2 in index 2 (the third item).
    # As well the read_1_count and read_2_count.
    entries[ID][int(read)] = str(file)
    entries[ID][int(read) + 2] = int(read_count)

# (Optional) Sort the dictionary by the sample ID.
sample = list(entries.keys())
sample.sort()
entries = {i: entries[i] for i in sample}

# Write the dictionary to tsv output.
with open(args.outtsv, 'w', newline='') as tsvfile:
    # Specify the delimiter as '\t' for a tsv file. It use ',' to create csv file by default.
    writer = csv.writer(tsvfile, delimiter='\t')
    # The header
    writer.writerow(['ID', 'read_1', 'read_2', 'read_1_count', 'read_2_count'])
    # The content
    for entry in entries.values():
        writer.writerow(entry)
