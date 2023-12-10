import random


def even(func):
    def inner(*args, **kwargs):
        if inner.count % 2:
            inner.count += 1
            return func(*args, **kwargs)
        else:
            inner.count += 1
            return None

    inner.count = 0
    return inner


@even
def print_hello(x):
    print("hello", x)


print('Result of @even decorator')
print_hello(1)
print_hello(2)
print_hello(3)
print_hello(4)


def clip(func):
    def inner(*args, **kwargs):
        return func(*args)
    return inner


@clip
def print_clip(x, y, z=0, s="~"):
    print(x, y, z, sep=s)


print()
print('Result of @clip decorator')
print_clip(1, 2, z=3, s="_")
print(1, 2, 3, sep="_")


def repeat(x):
    def decorator(func):
        def inner(*args, **kwargs):
            return tuple([func(*args, **kwargs) for _ in range(x)])
        return inner
    return decorator


@repeat(50)
def random_sum(n):
    return sum(random.random() for _ in range(n))


print()
print('Result of @repeat decorator')
print(random_sum(1_000_000))
print(len(random_sum(1_000_000)))


def cash(func):
    def inner(arg):
        if arg in inner.calls:
            return inner.calls[arg]
        else:
            inner.calls[arg] = func(arg)
            return func(arg)

    inner.calls = {}
    return inner


@cash
def fib(x):
    print(f"вызвана фунция Фибоначчи f({x})")
    if x < 2:
        return 1
    else:
        return fib(x-1) + fib(x-2)


def old_fib(x):
    if x < 2:
        return 1
    else:
        return old_fib(x-1) + old_fib(x-2)


print()
print('Result of @cash decorator')
fib(10)
print(fib(10))
old_fib(10)
