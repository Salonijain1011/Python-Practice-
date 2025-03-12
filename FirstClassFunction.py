def apply_functions(func1, func2, value):
    return (func1(value), func2(value))
def square(x):
    return x * x
def double(x):
    return x * 2
result = apply_functions(square, double, 5)
print(result) 