# Create a generator function that yields squares of numbers up to a given limit. 
def gen_square(n):
  for i in range(1,n+1):
    yield i**2
obj = gen_square(10)
for i in obj:
  print(i)