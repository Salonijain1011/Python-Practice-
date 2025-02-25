s = "python"
vowels = [char for char in s if char in 'aeiouAEIOU']
print(vowels)


# print permutation of cordinates of a cuboid where 0 <= i,j,k <= x,y,z
x = int(input())
y = int(input())
z = int(input())
n = int(input()) 
s = [[i,j,k] for i in range(x+1) for j in range(y+1) for k in range(z+1) if i+j+k!=n]
print(s)

