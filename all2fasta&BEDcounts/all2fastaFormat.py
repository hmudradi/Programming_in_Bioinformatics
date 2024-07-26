#! /usr/bin/env python3
import sys
import argparse
import os
import re

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--i", help="this is Input file")
parser.add_argument('-f', '--FOLD', type=int, default=70) 
args = parser.parse_args()
num = args.FOLD
if (args.i):
    inpfile = str(args.i)
    
def GB_fasta(fastaformat):
    num = 0
    with open(fastaformat, 'r') as gb_fa:
        fasta_lines = []
        fasta_rec = {}
        hb = 0
        for fasta_line in gb_fa:
            if (hb == 1):
                fasta_lines.append(fasta_line)
            if (fasta_line.strip() != ''):

                if (re.search(pattern='ACCESSION', string=fasta_line) != None):
                    fasta_rec["name"] = ">" + (fasta_line.split())[1].strip('\n')
                if (re.search(pattern='DEFINITION', string=fasta_line) != None):
                    fasta_rec["descr"] = (fasta_line.strip('\n').replace('DEFINITION', 'descr='))
                if (re.search(pattern='LOCUS', string=fasta_line) != None):
                    fasta_rec["len"] = fasta_line.split()[2].strip('\n')
                if (re.search(pattern='ORIGIN', string=fasta_line) != None):
                    hb = 1
                if (re.search(pattern='//', string=fasta_line) != None):

                    sequence = ''
                    for i in range(1, len(fasta_lines) - 1):
                        sequence += ''.join(fasta_lines[i].split()[1:])
                    fasta_rec["seq"] = sequence.upper().strip('\n')
                    if (len(re.findall(r'[^ATCGNatcgn]+', fasta_rec["seq"])) != 0):
                        num = 1
    return [fasta_rec], num

def Fastq_fasta(fastaformat):
    num = 0
    with open(fastaformat, 'r') as fq_fa:
        sequence = []

        for fasta_line in fq_fa:

            if (re.search(pattern='\\+', string=fasta_line) != None):
                fasta_rec = {}
            if (re.search(pattern='\\?', string=fasta_line) == None) and (re.search(pattern='@', string=fasta_line) != None):
                fasta_rec = {}
                fasta_rec['name'] = fasta_line.replace("@", ">").strip('\n')


            elif (re.search(pattern='\\?', string=fasta_line) ==None) and (
                    re.search(pattern='[ATCGn]+', string=fasta_line) != None):
                fasta_rec["seq"] = fasta_line.strip("\n")
                if (len(re.findall('[^ATCGNatcgn]+', fasta_rec["seq"])) != 0):
                    num = 1
                fasta_rec["len"] = len(fasta_line.strip("\n"))
                sequence.append(fasta_rec)
    return sequence, num


def EMBL_fasta(fastaformat):
    num = 0
    with open(fastaformat, 'r') as embl_fa:
        fasta_lines = []
        fasta_rec = {}
        hb = 0
        for fasta_line in embl_fa:
            if (hb == 1):
                fasta_lines.append(fasta_line)
            if (fasta_line.strip() != ''):

                if (re.search(pattern='ID', string=fasta_line) != None):
                    fasta_rec["name"] = ">" + (fasta_line.split())[1].strip('\n')
                if (re.search(pattern='DE  ', string=fasta_line) != None):
                    fasta_rec["descr"] = (fasta_line.strip('\n').replace('DE   ', 'descr='))
                if (re.search(pattern='SQ', string=fasta_line) != None):
                    hb = 1
                    fasta_rec["len"] = fasta_line.split()[2].strip('\n')

                if (re.search(pattern='//', string=fasta_line) != None):

                    sequence = ''
                    for i in range(1, len(fasta_lines) - 1):
                        sequence += ''.join(fasta_lines[i].split()[0:-1])
                    fasta_rec["seq"] = sequence.upper().strip('\n')
                    if (len(re.findall(r'[^ATCGNatcgn]+', fasta_rec["seq"])) != 0):
                        num = 1
    return [fasta_rec], num

def MEGA_fasta(fastaformat):
    num = 0
    with open(fastaformat, 'r') as mega_fa:
        fasta_lines = []
        header = []
        sequence = []
        for fasta_line in mega_fa:
            fasta_lines.append(fasta_line)
        content_list = ("".join(fasta_lines[2:])).split("#")
        for each in content_list:
            info = each.split("\n")

            header.append(info[0])
            sequence.append("".join(info[1:]))
    header = header[1:]
    sequence = sequence[1:]
    if (len(header) == 0):
        fasta_rec = {}
        fasta_rec["name"] = header[0].strip('\n')
        fasta_rec["seq"] = sequence[0].strip('\n')
        fasta_rec["len"] = len((sequence[0]).strip('\n'))
        sequence.append(fasta_rec)
    else:

        for i in range(0, len(header)):

            fasta_rec = {}
            fasta_rec["name"] = header[i].strip('\n')
            fasta_rec["seq"] = sequence[i].strip('\n')
            fasta_rec["len"] = len((sequence[i]).strip('\n'))
            if (len(re.findall(r'[^ATCGNatcgn]+', sequence[i])) != 0):
                num = 1
            sequence.append(fasta_rec)
    return [fasta_rec], num

def vcf_fasta(fastaformat):
    fasta_sample=[]
    sequence = []
    fasta_rec={}
    num = 0
    with open (fastaformat, 'r') as vcf_fa:
        for fasta_line in vcf_fa:
            ref=[]
            alt=[]
            genetype=[]
            if (fasta_line.startswith("#CHROM")):
                fasta_sample=fasta_line.strip("\n").split("\t")[9:]
                for i in fasta_sample:
                    fasta_rec[i]=""
            elif (fasta_line.startswith("##")):
                pass
            else:
                realgenetype=[]
                genetype_dict={}
                genetype=fasta_line.strip("\n").split("\t")[9:]
                ref=fasta_line.split("\t")[3]
                alt=fasta_line.split("\t")[4].split(",")
                for i in genetype:
                    if (i[0] == 0):
                        realgenetype.append(ref)
                    else:
                        realgenetype.append(alt[int(i[0])-1])
                for i in range(0,len(fasta_sample)):
                    genetype_dict[fasta_sample[i]]=realgenetype[i]
                    pass
                for j in genetype_dict:
                    fasta_rec[j]=fasta_rec[j]+genetype_dict[j]
                    pass
        for i in fasta_sample:
            fasta_rec["name"] = ">" + i
            fasta_rec["seq"] = "".join(fasta_rec.values())
        num = 0
        sequence.append(fasta_rec)
    return [fasta_rec], num


def sam_fasta(fastaformat):
    num = 0
    sequence=[]
    fasta_rec = {}
    with open (fastaformat, 'r') as sam_fa:
        for fasta_line in sam_fa:
            if (re.search(pattern = '@', string = fasta_line) ==None):
                num = 0
                cols=fasta_line.rstrip().split("\t")
                #print(cols[0])
                for i in cols:
                    fasta_rec["name"] = ( '>' + cols[0])
                    fasta_rec["seq"] = (cols[9])
                sequence.append(fasta_rec)
                num = 0
    return sequence, num

with open(inpfile, "r") as Inp:  # print(seq)
    first_fasta_line = Inp.readline()
    match_seq = re.search(pattern='@SQ', string=first_fasta_line)
    if (match_seq != None):
        print("sam file will be converted to fasta format")
        sequence, num = sam_fasta(inpfile)

    else:
        match_seq = re.search(pattern='ID', string=first_fasta_line)
        if (match_seq != None):
            sequence, num = EMBL_fasta(inpfile)
            print("embl file will be converted to fasta format")
            # print(seq)
        else:
            match_seq = re.search(pattern='LOCUS', string=first_fasta_line)
            if (match_seq != None):
                sequence, num = GB_fasta(inpfile)
                # print(seq)
                print("gb file will be converted to fasta format")
            else:
                match_seq = re.search(pattern='#MEGA', string=first_fasta_line)
                if (match_seq != None):
                    print("mega file will be converted to fasta format")
                    sequence, num = MEGA_fasta(inpfile)
                    # print(seq)
                else:
                    match_seq = re.search(pattern='@', string=first_fasta_line)
                    if (match_seq != None):
                        print("fastq file will be converted to fasta format")
                        sequence, num = Fastq_fasta(inpfile)
                    else:
                        match_seq = re.search(pattern='##', string=first_fasta_line)
                        if (match_seq != None):
                            print("vcf file will be converted to fasta format")
                            sequence, num = vcf_fasta(inpfile)
                        else:
                            print("Input file does not match_seq with any format")

#print(seq)
file_name = inpfile.split(".")
if (num == 0):
    extension = "fna"


else:
    extension = "faa"
if file_name[-1] == "fna" or file_name[-1] == "faa":
    output = ".".join(file_name)
    Output = open(output, "w")
elif len(file_name) == 1:
    ouput = file_name[0] + "." + extension
    Output = open(output, "w")
else:
    file_name[-1] = extension
    ouput = output = ".".join(file_name)
    Output = open(output, "w")

for fasta_rec in sequence:
    Output.write(str(fasta_rec['name']))
    Output.write("\n")

    n = 0
    for c in list(str(fasta_rec['seq'])):
        Output.write(str(c))
        n += 1
        if n > num:
            n = 0
            Output.write("\n")
    Output.write("\n")

