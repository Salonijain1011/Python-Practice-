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