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


# Find the next greater number , if not present in the list print(-1)
arr = [1,8,7,4,6,3,9,0,1]
a = []
for i in range(len(arr)):
  s = 'false' 
  for j in range(i+1,len(arr)):
    if arr[j]>arr[i]:
      a.append(arr[j])
      s = 'true'
      break
  if s == 'false':
    a.append(-1)
print(a)


#Method 2 (without flag)
a = [1,2,3,5,4]
b=[]
for i in range(len(a)):
  for j in range(i+1,len(a)):
    if a[j]>a[i]:
      b.append(a[j])
      break
  else:
     b.append(-1)
print(b)


# Input = [1,2,3,4,3,2,1,4]  output = [1,2,3,4,_,_,_,_]
#Method 1
lst = [1,2,3,4,3,4,1,2]
s = set(lst)
print(s)
i = list(s)
for x in range(4):
    i.append('_')
print(i)


#Method2
lst = [1,2,3,4,3,4,1,2]
lst2=[]
for i in lst:
    if i not in lst2:
        lst2.append(i)
    else:
        lst2.append('_')
print(lst2)


#Method 3
lst = [1,2,3,4,3,2,1,4]
for i in range(len(lst)):
    for j in range(i+1,len(lst)):
        if lst[j] == lst[i] and lst[j]!="_":
            lst[j]= "_"
print(lst)