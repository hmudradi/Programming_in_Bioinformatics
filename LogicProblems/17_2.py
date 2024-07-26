#!usr/bin/env python3
#shebang line
all_list=[]
    # list1
data = sorted([4, 5, 6, 2, 3,7,1,9,8])
n = len(data)
n = n // 2
    #list2
dat = sorted([2,4,5,6,8,9,6])
m = len(dat)
m = m // 2
#print a new list with both the outputs
all_list = data[n],dat[m]
print(all_list)
