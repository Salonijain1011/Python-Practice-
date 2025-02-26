#without using temp
a = 10
b = 6
print("Before swapping:",a,b)
a = a + b
b = a-b
a = a-b
print("After swapping:",a,b)


#using temp
num1 = 2
num2 = 3
print("before:",num1,num2)
temp = num1
num1 = num2 
num2 = temp
print("after:",num1,num2)