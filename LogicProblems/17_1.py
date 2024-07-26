#!usr/bin/env python3
#shebang line
def calculate(a,b):
    all_list=[]
    #input list1
    data = sorted(a)
    n = len(data)
    n = n // 2
    #input list2
    dat = sorted(b)
    m = len(dat)
    m = m // 2
    #print a new list with both the outputs
    all_list = data[n],dat[m]
    print(all_list)
calculate([4, 5, 6, 2, 3,7,1,9,8],[2,4,5,6,8,9,6])
