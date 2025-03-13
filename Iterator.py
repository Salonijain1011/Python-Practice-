# Write a class EvenNumbers that acts as an iterator, generating even numbers up to a given limit.
class EvenNumber:
  def __init__(self):
    self.num=2
  def __iter__(self):
    return self
  def __next__(self):
      if self.num<10 and self.num%2==0:
        val = self.num
        self.num+=2
        return val
      else:
        raise StopIteration
obj = EvenNumber()
for i in obj:
  print(i)    
  

# Create a class ReverseIterator that takes a list and iterates through it in reverse.
class ReverseIterator:
  def __init__(self):
    self.lst=[]
  def __iter__(self):
    return self
  def __next__(self):
    if self.lst:
      return self.lst.pop()
    else:
      raise StopIteration
obj = ReverseIterator()
obj.lst = [1,2,3,4,5]
for i in obj:
  print(i)  