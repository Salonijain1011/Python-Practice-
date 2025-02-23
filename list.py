a = [1,2,3,8,5]
b =[]
for i in a:
    c = 1
    for j in a:
        if j != i:
            c = c*j
        b.append(c)
    print(c)



my_list = [3, 1, 4, 1, 5, 9]
sorted_list = sorted(my_list)
print(sorted_list) 
print(my_list)      
my_list.sort()
print(my_list)