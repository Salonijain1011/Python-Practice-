# Given a list of tuples (name, age), sort the list by age using a lambda function.


people = [("Alice", 30), ("Bob", 25), ("Charlie", 35)]

sorted_people = sorted(people, key= lambda x:x[1])
print(sorted_people)