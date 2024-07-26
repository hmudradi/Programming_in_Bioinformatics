#!usr/bin/env python3
#shebang line
def Bal(st):  
    count= 0  
    a=False  
    for i in st:  
        if i == "{":  
            count += 1  
        elif i == "}":  
            count-= 1  
        if count < 0:  
            return a  
    if count==0:  
        return not a  
    return ans  
st=input("Enter a string of brackets: ")   
if Bal(st) == True:
   print("Yes")
else:
  print("No")
