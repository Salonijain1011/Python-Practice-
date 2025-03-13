# Write a generator function fibonacci(n) that yields the first n numbers in the Fibonacci sequence.
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b
fib = fibonacci(6)
print(list(fib))
    

# Write a generator prime_generator(n) that yields the first n prime numbers.
def prime_generator(n):
  for i in range(2,n+1):
    for j in range(2,i):
      if i%j==0:
        break
    else:
      yield i
f = prime_generator(8)
for i in f:
  print(i)