#Write a function that swaps keys and values in a dictionary.

dic1 = {'a': 1, 'b': 2, 'c': 3}
dic2 = {value: key for key, value in dic1.items()}
print(dic2)
