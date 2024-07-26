#!/usr/bin/env python3

import sys

match = +1
mismatch = -1
gap = -1

readseqq1 = sys.argv[1]
readseqq2 = sys.argv[2]
inpseq1 = ""
inpseq2 = ""
with open(readseqq1) as inpseq1_fh:
    for fastaline in inpseq1_fh.readlines():
        if fastaline.startswith(">"):
            continue
        else:
            inpseq1 += fastaline
with open(readseqq2) as inpseq2_fh:
    for fastaline in inpseq2_fh.readlines():
        if fastaline.startswith(">"):
            continue
        else:
            inpseq2 += fastaline
inpseq1 = inpseq1.rstrip("\n")
inpseq2 = inpseq2.rstrip("\n")

#Initializing the matrix to 0
a = len(inpseq1)
b = len(inpseq2)
c = []
for i in range(a+1):
    sw = []
    for j in range(b+1):
        sw.append(0)
    c.append(sw)


#Matrix filling
for i in range(1,a+1):
    for j in range(1, b+1):
        if inpseq1[i-1] == inpseq2[j-1]: 
            c[i][j] = max(0, c[i-1][j]+gap,c[i-1][j-1]+match,c[i][j-1]+gap)
        else:
            c[i][j] = max(0, c[i-1][j]+gap, c[i-1][j-1]+mismatch,c[i][j-1]+gap)

maxscorepc = 0 #maximum score per cell
for row in range(1, a+1):
    for column in range(1,b+1):
        if maxscorepc < c[row][column]:
            maxscorepc = c[row][column]     
            i = row                             
            j = column

#Backtracking 
bt1 = "" #empty string to backtrack for input seq 1
bt2 = "" #empty string to backtrack for input seq 2
while c[i][j] != 0:
    if inpseq1[i-1] == inpseq2[j-1]:
        bt1 += inpseq1[i-1]
        bt2 += inpseq2[j-1]
        i -= 1
        j -= 1
           
    elif inpseq1[i-1] != inpseq2[j-1]:
        sw = [c[i-1][j-1], c[i-1][j], c[i][j-1]] #above-left,above top, left 
        if max(sw) == sw[0]: # first element of the sw list
            bt1 += inpseq1[i-1]
            bt2 += inpseq2[j-1]
            i -= 1
            j -= 1

        elif max(sw) == sw[1]: # next element of the sw list
            bt1 += inpseq1[i-1]
            bt2 += "-"
            i -= 1

        elif max(sw) == sw[-1]: #last element of the list
            bt1 += "-"
            bt2 += inpseq2[j-1]
            j -= 1

# Reversing backtracked strings for alignment scoring   
swal1 = bt1[::-1]                   
swal2 = bt2[::-1]                   

#finding matches for local alignment
swmatch = ""
for i in range(len(swal1)):
    if swal1[i] == swal2[i]:
        swmatch += "|"
    elif swal1[i] != swal2[i]:
        if swal1[i] == "-" or swal2[i] == "-":
            swmatch += " "
        else:
            swmatch += "*"

#Scoring the matrix
swscore = 0
for i in range(len(swmatch)):
    if swmatch[i] == "*" or swmatch[i] == " ":
        swscore += gap
    elif swmatch[i] == "|":
        swscore += match

#stdout the final alignment
sys.stdout.write(str(swal1) + "\n" + str(swmatch) + "\n" + str(swal2) + "\n" + "Alignment Score:" + str(swscore) + "\n")

