#!/usr/bin/env python3
import sys
import argparse

parser = argparse.ArgumentParser() 
# Designing command line
parser.add_argument("-i",'--i', help="input .bed file") 
args = parser.parse_args()
list_values = []

with (open(args.i, 'r') as file_open):
    # Opening the file and adding all the values to a list_values
    for l in file_open:
        column_values = l.rstrip().split("\t")
        list_values.append(column_values)

# Assigning values to chromosome, start and start from the list_values file
chrom = ""
num = 0      
while (num < len(list_values)):
    chrom = list_values[num][0]
    start = int(list_values[num][1])
    stop  = int(list_values[num][2])
    coord = []
    # Comparing opening and closing coords with the same chromosomes    
    while(num < len(list_values) and list_values[num][0] == chrom):
        coord.append((int(list_values[num][1]), -1)) # Assigning -1 to the coord-start as a tuple
        coord.append((int(list_values[num][2]), 1))  # Assigning 1 to the coord-stop as a tuple
        num += 1 
    coord.sort()

count = 1
for i in range(1, len(coord)):
    if(coord[i - 1][0] <= coord[i][0]):
    # Printing and counting keeping the start-coord inclusive and stop-coord exclusive
      if(coord[i - 1][0] != coord[i][0] and count > 0):
        print(chrom, coord[i - 1][0], coord[i][0], count, sep='\t')
      if (coord[i][1] == -1):
         count += 1
      else:
           count -= 1
    else:
        print("ERROR MESSAGE")
