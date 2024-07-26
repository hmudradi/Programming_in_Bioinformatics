#!usr/bin/env python3
#shebang line
def isBioPalindrome(s):
    comp=[]
    strr=[]
    strr = s[::-1]
    for i in strr:
        if i == "T":
            comp.append("A")
        if i == "A":
            comp.append("T")
        if i == "G":
            comp.append("C")
        if i == "C":
            comp.append("G")
    return ''.join(comp)
    if(s==comp):
        return True
    return False
bp = input("Enter a DNA seq:")
ans = isBioPalindrome(bp)
 
if ans:
    print("Is a Biological Palindrome")
 
else:
    print("Is NOT a Biological Palindrome")

 

