
# Given a list of tuples (name, age), sort the list by age using a lambda function.

people = [("Alice", 30), ("Bob", 25), ("Charlie", 35)]
sort = sorted(people, key= lambda x:x[1])
print(sort)


# sort a dictionary by value
dic = {'a':1,'b':3,'c':2}
s = sorted(dic.items(), key = lambda x:x[1])
print(dict(s))


# Print i and square of i in dictionary
s= {x:x**2 for x in [1,2,3,4]}
print(s)

       