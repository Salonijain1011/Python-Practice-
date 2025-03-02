# Convert a string to a dictionary where characters are keys and their occurrences are values.

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