#!/usr/bin/env python3

import sys

match = 1
mismatch = -1
gap = -1


# Input FASTA sequences
readinp1 = sys.argv[1]
readinp2 = sys.argv[2]
inp1 = ""
inp2 = ""

with open(readinp1) as inp1_fh:
    for line in inp1_fh.readlines():
        if line.startswith(">"):
            continue
        else:
            inp1 += line

with open(readinp2) as inp2_fh:
    for line in inp2_fh.readlines():
        if line.startswith(">"):
            continue
        else:
            inp2 += line
inp1 = inp1.rstrip("\n")
inp2 = inp2.rstrip("\n")

a = len(inp1)
b = len(inp2)
c = []

# Filling first row and col
for i in range(a+1):
    nw = []
    for j in range(b+1):
        nw.append(0)
    c.append(nw)
for j in range(b+1):
    c[0][j] = gap*j

for i in range(a+1):
    c[i][0] = gap*i


# filling the matrix
for i in range(1, a+1):
    for j in range(1, b+1):
        if inp1[i-1] == inp2[j-1]:
            c[i][j] = max(c[i][j-1]+gap, c[i-1][j]+gap, c[i-1][j-1]+match)
        else:
            c[i][j] = max(c[i][j-1]+gap, c[i-1][j]+gap, c[i-1][j-1]+mismatch)

# Backtracing
bt1 = ""
bt2 = ""
i = a
j = b

while (i>0 or j>0):

    if inp1[i-1] == inp2[j-1]:
        bt1 += inp1[i-1]
        bt2 += inp2[j-1]
        i -= 1
        j -= 1

    elif inp1[i-1] != inp2[j-1]:
        temp = [c[i-1][j-1], c[i-1][j], c[i][j-1]]        
 
        if max(temp) == temp[0]:
            bt1 += inp1[i-1]
            bt2 += inp2[j-1]
            i -= 1
            j -= 1

        elif max(temp) == temp[1]:
            bt1 += inp1[i-1]
            bt2 += "-"
            i -= 1

        elif max(temp) == temp[-1]:
            bt1 += "-"
            bt2 += inp2[j-1]
            j-=1

 # Reversing strings for alignment scoring  
bt1 = bt1[::-1]                   
bt2 = bt2[::-1]  

#finding matches for global alignment
nwmatch = ""
for i in range(len(bt1)):
    if bt1[i] == bt2[i]:
        nwmatch += "|"
    elif bt1[i] != bt2[i]:
        if (bt1[i] == "-" or bt2[i] == "-"):
            nwmatch += " "
        else:
            nwmatch += "*"

#Scoring the alignment
nwscore = 0
for i in range(len(nwmatch)):
    if (nwmatch[i] == "*" or nwmatch[i] == " "):
            nwscore += gap    
    elif nwmatch[i] == "|":
            nwscore += match


#stdout the final alignment
sys.stdout.write(str(bt1) + "\n" + str(nwmatch) + "\n" + str(bt2) + "\n" + "Alignment Score:" + str(nwscore) + "\n")




