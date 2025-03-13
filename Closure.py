# Create a function counter(start) that returns a function that, when called, increments and returns the count.
def counter(start):
    def inner():
        nonlocal start
        start +=1
        return start
    return inner
count_from_5 = counter(5)
print(count_from_5())  
print(count_from_5())  
print(count_from_5()) 


# Write a function multiplier(factor) that returns a function that multiplies any input by factor.
def multiplier(factor):
    def inner(number):
        return number * factor
    return inner
a = multiplier(3)
print(a(5)) 
print(a(10))  
