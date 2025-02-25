#  Write a function that prints all positional arguments and keyword arguments.


def print_args_kwargs(*args, **kwargs):
    print("Positional Arguments:")
    for arg in args:
        print(arg)

    print("Keyword Arguments:")
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_args_kwargs(1, 2, 3, name="Alice", age=25)
