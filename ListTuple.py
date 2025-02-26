#convert list to tuple without using tuple()
a = [1,2,3]
tup = (*a,)
print(tup)
print(type(tup))

#convert tuple to list 
t = (1, 2, 3, 4)
a = list(t)
print(a)
print(a.append(4))

#concate two tuples
s = (1,2,3)
c = (4,5,6)
d = (s+c)
print(d)

#repeat a tuple 3 times
tup1 = (1,2,3)
print(tup1*3)

#check if all element in tuple are same
# t = (1,1,1,1)
# a=t[0]
# if x != a:
#     print('false')
# else:
#     print('true')

