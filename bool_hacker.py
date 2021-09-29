from inspect import signature
from typing import Callable


def f(a, b, c):
    return a and (b or c)


def hack(function: Callable):
    print(signature(function))


hack(f)
