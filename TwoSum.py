# Find the pair of two numbers whose sum is 7

a = [1,2,3,4,5,6,6,7,8]
b = []
for i in a:
    for j in a:
        if j+i == 7:
            if (j,i) not in b:
                b.append((i,j))
print(b)