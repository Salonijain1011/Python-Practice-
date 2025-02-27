#input = 'my name is saloni jain and output needs to be MY NamE IS SalonI JaiN
string = 'my name is saloni jain'
s = string.title()
d = s.split()
x = []
for i in d:
    w = i[0:-1] + i[-1].upper()
    x.append(w)
print(x,end = ' ')


#Method 2
string = "my name is saloni jain"
d = string.split()
s=[]
for i in d:
  a = i[0].upper() +i[1:-1] + i[-1].upper()
  s.append(a)
print(s,end=' ')


#Reverse each word in a sentence (keeping word order intact)
string = 'hello world'
s = string.split()
for i in s:
  a = i[::-1]
  print(a,end=' ')
  
  
# Remove vowels from a string.
vowels =['a','i','o','e','u']
string = 'python programming'
for i in string:
  if i in vowels:
    string = string.replace(i,'')
print(string)


#Find the first non-repeating character in a string.
# Input: "aabbccdeeffg"
# Output: "d"
string = 'aabbccdeeffg'
freq = {}
for i in string:
  if i in freq:
    freq[i]+=1
  else:
    freq[i]=1
for i in string:
      if freq[i] == 1:
        print(i)
        break