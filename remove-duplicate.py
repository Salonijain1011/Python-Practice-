list = [1,2,3,1,3,4,5]
list2 = []
for i in list:
  if i in list2:
    continue
  else:
    list2.append(i)
print(list2)