# Find the most frequent element in a list [1, 2, 2, 3, 3, 3, 4, 4]

lst = [1, 2, 2, 3, 3, 3, 4, 4]
freq = {}
for i in lst:
  if i in freq:
    freq[i]+=1
  else:
    freq[i]=1
max = 0  
for value in freq.values():  
    if value > max:  
        max = value
print(max)


# Find all duplicates in a list [1, 2, 3, 4, 5, 2, 3, 6]

lst = [1, 2, 3, 4, 5, 2, 3, 6]
a =[]
for i in lst:
  if i not in a:
    q=a.append(i)
  else:
    print(i,end=' ')