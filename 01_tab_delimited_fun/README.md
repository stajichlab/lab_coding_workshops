Problem description
====
This problem is focused around generation of tab delimited file/data out of some other computed information. 
The first example focuses on generating a manifest file based on the input.

Create a manifest tab-delimited file based on the names of files in the folder. Add a column that counts the number of reads in each file.
So the output should look like this for the `fastq` folder;

Write a tool that will run like this. Optionally have it provided a `-o output.tsv` to save the results to a file, otherwise just print to the screen.
```
make_manifest_from_fastq.py -i fastq
```

```
SampleID  Read_1  Read_2 Read_1_Count Read_2_Count
A  Sample_A_S1_R1_L001.fastq.gz Sample_A_S1_R2_L001.fastq.gz  1 1
B Sample_B_S2_R1_L001.fastq.gz  Sample_B_S2_R2_L001.fastq.gz  3 3
```
