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

      
# Given a string (a2b3c2) print output (aabbbcc)          
s = "a2b3c2"
a =[]
for i in range(0,len(s)-1,2):
      char = s[i]
      count = int(s[i + 1])
      a.append(char*count)
print(''.join(a))


# Given input (aa2b38cd4) output(aa*4b*38cd*4)
s = "aa2b38cd4"
result =[]
temp = ""
num = ""
for char in s:
        if char.isalpha(): 
            if num: 
                result.append(temp * int(num))
                temp = "" 
                num = ""   
            temp += char 
        elif char.isdigit(): 
            num += char
if temp:
    if num:
            result.append(temp * int(num))
    else:
            result.append(temp)
print("".join(result)) 


# Modify the given string by inserting * before and after numbers.
# Input: "hello23world9"
# Output: "hello*23*world*9*"

string = "hello23world9"
result=[]
temp=""
num = ""
for i in string:
    if i.isdigit():
        if temp: 
            result.append(temp)
            result.append('*')
            temp = "" 
        num += i
    elif i.isalpha(): 
        if num:
            result.append(num)
            result.append('*')
            num = ""
        temp += i
if num:
    result.append(num)
    result.append('*')
elif temp:
    result.append(temp)
print("".join(result))


# Capitalize Every Third Letter in a String
# Input: "this is a sample text"
# Output: "thIs is A saMple teXt"

string = "this is a sample text"
s = string.split()
a = []
for i in s:
    if len(i)>2:
      c = i[0:2] +i[2].upper() +i[3:]
    else:
      c=i
    a.append(c)
print(' '.join(a))