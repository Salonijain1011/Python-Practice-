s = 'hello'
a = ''
for i in range(len(s)-1,-1,-1):
    a += s[i]
print(a)


# reverse words in string
string="my name is saloni jain"
s=string.split()[::-1]
l=[]
for i in s:
  l.append(i)
# print(l)
print(" ".join(l))
  