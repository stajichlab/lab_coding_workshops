#!/usr/bin/env python
"""Generate a tab delimited manifest from a folder of FASTQ files"""
import argparse
import csv
import sys
import os
import re
import gzip

name_patterns = [r'(\w+)_S\d+_R([12])_L\d+',
                 r'^(\S+)_R?([12])\.',
                 r'^(\S+)_pair([12])\.']


def main():
    """Generate a manifest file from input folder."""
    # arg parse takes command-line arguments
    # like --input INFILE --output manifest.tsv
    parser = argparse.ArgumentParser(
        prog='make_manifest.py',
        description='Generate a manifest file from a folder of FASTQ files',
        epilog='Run on a folder as input')
    # this will take the argument --input (or -i) as name of directory to read
    parser.add_argument('-i', '--input', required=True, type=str,
                        help='Input folder')
    # this will take the argument --output (or -o) to save the manifest results
    # if not provided this it will default to writing to STDOUT
    parser.add_argument('-o', '--output',
                        type=argparse.FileType('w'),
                        default=sys.stdout,
                        help='Output file to save manifest (default STDOUT)')
    # sets the delimiter in how manifest is written out (default is tab)
    parser.add_argument('-d', '--delimiter', default="\t",
                        help='Output file delimiter (default \\t)')
    args = parser.parse_args()
    # everything before this is for parsing cmdline arguments
    # if you didn't like this part you could just set input directory
    # another way but the variables
    # args.output == output file stream
    # args.input == input directory
    # args.delimiter == output delimiter

    # store the file data in a dictionary
    data = {}
    # create an output writer for the CSV/TSV results
    csvout = csv.writer(args.output, delimiter=args.delimiter)
    # open the directory to read with os.listdir() which returns
    # a list of files
    # use the for loop to iterate through these
    for file in os.listdir(args.input):
        # check for files which end with the pattern of
        # .FASTQ .fq .FQ .fastq and optionally + .gz
        # the $ means the string has to end with this pattern
        # we are using regular expression library (re)
        rc = re.search(r'(\S+)\.(FASTQ|fq|FQ|fastq)(\.gz)?$', file)
        # after running the regex we get a result, if it matched
        # the 'if rc' will return true
        if rc:
            # lets setup some variables which will store the info
            # we will parse from sample name and forward or reverse
            # strand info
            samplename = None
            direction = None
            # this loops through the patterns created at the top of
            # the script which are the different ways files might
            # be named
            for pattern in name_patterns:
                # two values are captured in the patterns one is sample
                # name and one is read direction
                r2 = re.match(pattern, file)
                if r2:
                    # further handle the idea that files could be named
                    # SampA or Sample_A
                    # the re.sub does a replacement to remove
                    # Samp or Sample_ from the name
                    samplename = re.sub(r'Samp(le_?)?', '', r2.group(1))
                    direction = r2.group(2)
                    break
            if not samplename:
                print(f"cannot find pattern match for filename: {file}")
                continue
            if samplename not in data:
                data[samplename] = {direction: file}
            else:
                data[samplename][direction] = file
            fh = None
            if file.endswith(".gz"):
                fh = gzip.open(os.path.join(args.input, file), "rt")
            else:
                fh = open(os.path.join(args.input, file), "rt")
            if fh:
                linecount = 0
                for line in fh:
                    if len(line) > 1:
                        linecount += 1
            data[samplename][f'count_{direction}'] = int(linecount / 4)
        else:
            # otherwise our filename did not match the pattern looking
            # for those ending in fastq/FASTQ and .gz
            print(f'no match {file}')
    csvout.writerow(['SampleID', 'Read_1', 'Read_2',
                     'Read_1_Count', 'Read_2_Count'])

    for sample in sorted(data):
        csvout.writerow([sample,
                        data[sample]['1'],
                        data[sample]['2'],
                        data[sample]['count_1'],
                        data[sample]['count_2']])

    return 0


if __name__ == "__main__":
    main()
