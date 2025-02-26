def max_array(arr,n):
    max=arr[0]
    for i in range(1,n):
        if arr[i]>max:
            max=arr[i]
    return max
arr = [1,2,5,3,7,4]
n=len(arr)
largest = max_array(arr,n)
print(largest)
