#!usr/bin/env python3
#shebang line
# Python program to swap two variables

a = 10
b = 30

# To take inputs from the user
#a = input('Enter value of a: ')
#b = input('Enter value of b: ')

# create a temporary variable and swap the values
temp = a
a = b
b = temp

print('The value of a after swapping:',a)
print('The value of b after swapping: {}'.format(b))

