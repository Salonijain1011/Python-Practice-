#Convert a tuple of tuples into a dictionary.
#Input: ((1, "a"), (2, "b"), (3, "c"))
#Output: {1: "a", 2: "b", 3: "c"}

tup=((1, "a"), (2, "b"), (3, "c"))
dic = {key:value for key, value in tup}
print(dic)

