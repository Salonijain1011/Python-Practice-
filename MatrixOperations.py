#Transpose of a matrix

import numpy as np
matrix = np.array([[1, 2], [3, 4]])
print(matrix.T)

#Matrix Operations

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print(A + B)  
print(A * B)  
print(np.dot(A, B))  


#Rotate matrix by 90 degrees

def rotate_matrix(matrix):
    return np.rot90(matrix,k=1) 

matrix = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 9]]

print(rotate_matrix(matrix))

