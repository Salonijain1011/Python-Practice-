# Sum of numbers in string

s = '1,2,3,4'
d = s.split(',')
for i in range(len(d)):
      d[i] = int(d[i])
print(sum(d))