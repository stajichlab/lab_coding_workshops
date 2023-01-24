#!/usr/bin/env python
"""Generate a tab delimited manifest from a folder of FASTQ files"""
import argparse
import csv
import sys
import os
import re
import gzip

name_patterns = [ r'(\w+)_S\d+_R([12])_L\d+',
            r'^(\S+)_R?([12])\.',
            r'^(\S+)_pair([12])\.'
]


def main():
    """Generate a manifest file from input folder."""
    parser = argparse.ArgumentParser(
        prog='make_manifest.py',
        description='Generate a manifest file from a folder of FASTQ files',
        epilog='Run on a folder as input')
    parser.add_argument('-i', '--input', required=True, type=str,
                        help='Input folder')
    parser.add_argument('-o', '--output',
                        type=argparse.FileType('w'),
                        default=sys.stdout,
                        help='Input folder')
    parser.add_argument('-d', '--delimiter', default="\t",
                        help='Output file delimiter (default \\t)')
    args = parser.parse_args()
    data = {}
    csvout = csv.writer(args.output, delimiter=args.delimiter)
    for file in os.listdir(args.input):
        rc = re.search(r'(\S+)\.(FASTQ|fq|FQ|fastq)(\.gz)?$', file)
        if rc:
            samplename = None
            direction = None
            for pattern in name_patterns:
                r2 = re.match(pattern, file)
                if r2:
                    samplename = re.sub(r'Samp(le_?)?', '', r2.group(1))
                    direction = r2.group(2)
                    break
            if not samplename:
                print(f"cannot find pattern match the info in filename: {file}")
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
