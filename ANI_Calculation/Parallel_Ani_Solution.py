#!/usr/bin/env python3
import argparse
import os
import subprocess
import multiprocessing 

#global bb
# bb = []

# def append_to_global_array(value):
#     global bb
#     bb.append(value)


def calculate_diff(d):
     bb = []
     cmd = 'dnadiff -p {}{}result {} {}'.format(d[0], d[1], d[0], d[1])
     f = subprocess.check_call(cmd.split())
     with open(d[0]+d[1]+"result.report", "r") as f:
          x = f.readlines()[18]
          a=x.split(",")
          fields = a[0].split()
          value = fields[1]
          bb.append(value)
          # append_to_global_array(value)
          # print(bb)
          # print("LOL")
          # cc = bb
          return bb
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--o', help="Output file name")
    parser.add_argument('-t', '--t', help="Number of threads to be used for the program")
    parser.add_argument('file', nargs='+')
    args = parser.parse_args()
    t = int(args.t)
    out = args.o
    ff = args.file
    pool = multiprocessing.Pool(t)
    #final = [(ff[i], ff[j]) for i in range(len(ff)) for j in range(len(ff))]
    #  not considering the case where same file is taken in both indices
    final = []
    for i in range(len(ff)):
        for j in range(len(ff)):
            if i != j:
                final.append((ff[i],ff[j]))
                
    x = list(pool.map(calculate_diff, final))

    p = []
    
    for idx, i in enumerate(x):
        if idx % len(ff) == 0:
            p.append(['100.00'])
        p.append(i)
    p.append(['100.00'])

    single_list = [item for sublist in p for item in sublist]
   
    n=len(ff)
    mat = []
    while single_list != []:
       mat.append(single_list[:n])
       single_list = single_list[n:]
    
    #adding top row
    mat = [ff] + mat
    
# adding first column
    headers_mod = ['            '] + ff
    new_arr = [[headers_mod[i]]+mat[i] for i in range(n+1)]
    
    # Open a file for writing
    f = open(out, "w")

# Iterate over the elements of new_arr
    for i in new_arr:
    # Use the file keyword argument to print the elements of i to the file
        print(*i, file=f)

# Close the file
    f.close()

    for k in final:
        remove = "rm -rf {}genome*".format(k[0])
        try:
            os.system(remove)
        except FileNotFoundError:
            pass  # file doesn't exist, do nothing
    
    
