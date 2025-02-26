def fibonacci (n):
    a,b = 0,1
    for _ in range(n):
        print(a,end=' ')
        a,b = b,a+b
fibonacci(10)

#Using Recursion

def Fibonacci(n):
    if n <= 1:
        return n
    return Fibonacci(n - 1) + Fibonacci(n - 2)

print(Fibonacci(6)) 
