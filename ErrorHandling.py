# Handling ZeroDivisionError, ValueError
try:
    a = int(input("Enter a number: "))
    b = int(input("Enter another number: "))
    print(a / b)
except (ZeroDivisionError, ValueError) as e:
    print("Error:", e)
finally:
    print("Cannot divide by zero.")


# Handling FileNotFoundError
try:
    f = open('exal.txt','r')
    content = f.read()
    print(content) 
except FileNotFoundError as e:
    print('error',e)
finally:
    print('file closed')

    
# Write a program that takes a list of numbers and an index from the user. Return the element at that index. Handle IndexError if the index is out of range.
try:
 lst = input("Enter: ").split()
 index = input("Enter: ")
 index = int(index)
 name = lst[index]
 print(name)
except IndexError:
  print("error")
  
  
# Write a function validate_age(age) that asserts age >= 18. If the assertion fails, return "Invalid age!". 
def set(age):
  try:
    assert age >= 18, "Invalid age"
    return "Age is valid"  
  except AssertionError as e:
    print(e)
print(set(20))
print(set(16))