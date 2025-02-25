#Take string as input and print dictionary where character in string will 
# be keys and frequency of character will be the value

def string_dic(s):
  dic={}
  for char in s:
    if char !=" ":
      if char not in dic:
        dic[char]=1
      else:
        dic[char]+=1
  return dic
s = input('enter')
print(string_dic(s))