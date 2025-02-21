import copy
list1 = [1,2,3]
list2 = [list1]
list3 = copy.deepcopy(list2)
print(list2)
print(list3)
list1.append(4)
print(list2)
print(list3)