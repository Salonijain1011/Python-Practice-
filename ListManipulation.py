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
    
    
#Find pairs in a list that sum to a target value.
# Input: arr = [1, 2, 3, 4, 5], target = 6
# Output: [(1,5), (2,4)]
arr = [1, 2, 3, 4, 5]
a =[]
for i in arr:
  for j in arr:
    if i+j == 6 and (j, i) not in a:
      if i==j:
        break
      a.append((i,j))
print(a)


#Flatten a nested list.
#Input: [[1, 2, [3, 4]], [5, 6], 7]
#Output: [1, 2, 3, 4, 5, 6, 7]
lst = [[1, 2, [3, 4]], [5, 6], 7]
for sublist in lst:
   if type(sublist)==int:
      print(sublist) 
   else: 
    for x in sublist:
      if type(x)==int:
        print(x)
      elif type(x)==list:
        for i in x:
          print(i)
          
          
#Method 2
l = [[1,2],[3,4],5]
output = [item for sublist in l for item in (sublist if isinstance(sublist,list) else [sublist])]
print(output)          
