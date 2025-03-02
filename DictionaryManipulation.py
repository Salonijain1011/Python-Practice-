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


#Merge two dictionary
d1 = {'a': 1, 'b': 2}
d2 = {'b': 3, 'c': 4}
print(d1 | d2)


#Find the key with the maximum value.
# Input: {'Alice': 88, 'Bob': 75, 'Charlie': 90}
# Output: "Charlie"
dic = {'Alice': 88, 'Bob': 75, 'Charlie': 90}
max_value=0
max_key = None
for key,value in dic.items():
  if value > max_value:
   max_value = value
   max_key=key
print(max_key)


#Find the sum of all dictionary values.
# Input: {'x': 10, 'y': 20, 'z': 30}
# Output: 60
dic = {'x': 10, 'y': 20, 'z': 30}
sum = 0
for key,value in dic.items():
  sum += value
print(sum)