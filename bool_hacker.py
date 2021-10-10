def f(a, b, c):
    return a and (b or c)


def hack(function):
    #    argcount = function.__code__.co_argcount
    arguments = function.__code__.co_varnames
    generate_table(arguments)
    # print(arguments)


def generate_table(arguments):
    table = [[0] * (len(arguments) + 1) for i in range(2 ** len(arguments))]
    for i in range(len(table)):
        print(table[i])


hack(f)
