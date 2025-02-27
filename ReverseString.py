#Method 1
s = 'hello'
a = ''
for i in range(len(s)-1,-1,-1):
    a += s[i]
print(a)

#Method 2
def reverse_string(s):
    return s[::-1]
print(reverse_string("hello"))


# reverse words in string
string="my name is saloni jain"
s=string.split()[::-1]
l=[]
for i in s:
  l.append(i)
# print(l)
print(" ".join(l))
 
  
# Write a program to print reverse of odd index string element i.e. "hello good morning saloni" to "hello doog morning inolas". 

string_input = 'hello good morning saloni'
d = string_input.split()
for i in range(len(d)):
  if i%2!=0:
    d[i] = d[i][::-1]
output = ' '.join(d)  
print(output)
  

