#Write a function that swaps keys and values in a dictionary.

dict1 = {'a': 1, 'b': 2, 'c': 3,'d':3}
dict2 = {value: key for key, value in dict1.items()}
print(dict2)


# To handle duplicate values 

dic1 = {'a': 1, 'b': 2, 'c': 3,'d':3}
dic={}
for key,value in dic1.items():
  if value not in dic:
    dic[value]=key
  else:
    dic[value]=list(dic[value])
    dic[value].append(key)
print(dic)