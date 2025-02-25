#Write a function that accepts a tuple of numbers and returns a new tuple containing only the even numbers.
def even_tup (n):
  a =[]
  for i in n:
    if i%2==0:
      a.append(i)
  return tuple(a)
n = (1,2,3,4,5,6)
print(even_tup(n))