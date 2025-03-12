# Create a closure function that generates a series of numbers starting from a given base.
def outer(x):
  def inner():
    nonlocal x
    x+=1
    return x
  return inner
new = outer(10)
print(new())
print(new())