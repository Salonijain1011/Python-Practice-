
a = [1,2,3,8,5]
b =[]
for i in a:
    c = 1
    for j in a:
        if j != i:
            c = c*j
        b.append(c)
    print(c)


# Write a function that takes a comma-separated string of numbers and converts it into a list of integers.

def str_list(s):
    return list(map(int,s.split(',')))

print(str_list("1,2,3,4,5")) 



my_list = [3, 1, 4, 1, 5, 9]
sorted_list = sorted(my_list)
print(sorted_list) 
print(my_list)      
my_list.sort()
print(my_list)