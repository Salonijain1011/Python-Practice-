#Write a function that returns the union, intersection, and difference of two sets.

def set_operations(set1, set2):
    return (
        set1.intersection(set2),  
        set1.union(set2),         
        set1.difference(set2),    
        set2.difference(set1)     
    )

result = set_operations({1, 2, 3}, {2, 3, 4})
print(result)


        
        

                   