# Write a program to print second largest element from an array.

def second_largest(arr):
    return sorted(set(arr))[-2]

print(second_largest([12, 35, 1, 10, 34, 1]))
