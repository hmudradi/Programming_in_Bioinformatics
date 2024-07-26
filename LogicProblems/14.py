#!usr/bin/env python3
#shebang line
def fibonacci(n):
    a, b = 0, 1
    for i in range(n):
        yield a
        a, b = b, a + b
print (list(fibonacci(8)))

