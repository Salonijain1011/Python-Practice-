# Sort only the even indexed element from a given list
l = [4,1,2,3]
res = l
even = sorted([l[i] for i in range(len(l)) if i % 2 == 0])
a = 0
for i in range(len(l)):
  if i%2==0:
      res[i] = even[a]
      a+=1 
print(res)


# Print those string that are a substring in other
s = ["mass","as","hero","superhero","mass","per"]
a =[]
for i in s:
  for j in s:
    if j!=i and j in i:
      a.append(j)
print(a)


# Find Words Containing Character
a = ["abc","bcd","aaaa","cbc"]
s=[]
indexes=[]
for idx,i in enumerate(a):
  if "b" in i:
    s.append(i)
    indexes.append(idx)
print(indexes)


# Count the Number of Vowel Strings in Range
words = ["are","amy","u"]
a =[]
vowels=['a','i','o','e','u']
for i in words:
  if i[0] in vowels and i[-1] in vowels:
    a.append(i)
print(a)


# Maximum Number of Words Found in Sentences
s = ["alice and bob love leetcode", "i think so too", "this is great thanks very much"]
a = []
b = 0
for i in s:
  if len(i)> b:
    b = len(i)
    a = i
# print(a)
k = a.split()
print(len(k))


#TwoSum Elements
# Find the pair of two numbers whose sum is 7
a = [1,2,3,4,5,6,6,7,8]
b = []
for i in a:
    for j in a:
        if j+i == 7:
            if (j,i) not in b:
                b.append((i,j))
print(b)


#Find the first duplicate and first non-duplicate element 
s = "abcadfebca"
a = []
# for i in s:
#     if i not in a:
#           a.append(i)
#     break
# print(a)
freq={}
for i in s:
    if i in freq:
        freq[i]+=1
    else:
        freq[i]=1
print(freq)
for i in s:
    if freq[i]==1:
        print(i)
        break
for i in s:
    if freq[i]>1:
        print(i)
        break


# output [0,0,0,0,1,1,1]
s = [0,0,0,1,1,0,1]
i =0
j = len(s)-1
while i<j:
    if s[i]==0 and s[j]==1:
        i+=1
        j-=1
    elif s[i]==1 and s[j]==0:
        s[i],s[j]=s[j],s[i]
        i+=1
        j-=1
    elif s[i]==0 and s[j]==0:
        i+=1
    elif s[i]==1 and s[j]==1:
        j-=1
print(s)


# s = [0,1,0,2,1,0,1,2,0]
# output = [0, 0, 0, 0, 1, 1, 1, 2, 2]
s = [0,1,0,2,1,0,1,2,0]
i=0
j=0
k=len(s)-1
while j<=k:
  if s[j]==0:
    s[i],s[j]=s[j],s[i]
    i+=1
    j+=1
  elif s[j]==1:
    j+=1
  else:
    s[j],s[k]=s[k],s[j]
    k-=1
print(s)


# input = s = [1,3,4,8]
# input = a = [2,5,6]
# Merge Sorted Array
s = [1,3,4,8]
a = [2,5,6]
res=[]
i=0
j=0
while i<len(s) and j<len(a):
  if s[i]<a[j]:
    res.append(s[i])
    i+=1
  else:
    res.append(a[j])
    j+=1
while i<len(s):
  res.append(s[i])
  i+=1
while j<len(a):
  res.append(a[j])
  j+=1
print(res)


# Merge Sorted Array without including zero
s = [1,2,3,0,0,0]
a = [2,5,6]
res=[]
i=0
j=0
while i<len(s) and j<len(a):
  if s[i]<a[j]:
    res.append(s[i])
    i+=1
  else:
    res.append(a[j])
    j+=1
while i<len(s):
  res.append(s[i])
  i+=1
while j<len(a):
  res.append(a[j])
  j+=1
k=0
while k<len(res):
  if res[k]==0:
    res.pop(k)
  else:
    k+=1
print(res)


# Put all 0's at the right
s = [0, 1, 0, 3, 12] 
i=0
for j in range(len(s)):
  if s[j]!=0:
    s[i],s[j]=s[j],s[i]
    i+=1
print(s)