def f(a, b, c):
    return a and (b or c)


def medium4(a, b, c, d, e, f):
    return a and not b or c and not d and e and f


def logic1(a, b, c):
    return a and b and c or a and b and not c


def logic2(a, b, c):
    return (not a or b) and not (a or b) and (not a or c)


def medium2(a, b, c, d, e):
    return a and b or (b and not a) or (c and e) or (not c and e) or (c and not e) or (not c and not e)


def medium3(a, b, c, d, e):
    return (a and b) and (b and not a) or (c and e) and (not c and e) or (c and not e) or (not c and not e)


def hack(function):
    arguments = function.__code__.co_varnames
    print("Таблица истинности: ")
    generate_truth_table(arguments, function)
    print()
    print("Совершенная дизъюнктивная нормальная функция: ")
    print(generate_sdnf(arguments, function))
    print()
    print("Упрощённая сднф: ")
    generate_simplified_sdnf(arguments, function)


def generate_truth_table(arguments, function):
    # генерация таблциы
    table = generate_table(arguments, function)

    # объявление сепараторов

    column_separator = "┃"
    corner_separator = '╋'
    row_separator = '━'

    row_separator_array = []
    for i in range(len(arguments) + 1):
        row_separator_array.append(row_separator + corner_separator)
    row_separator_array.insert(0, corner_separator)

    # алгоритм вставки строки для вертикального разделения
    index = 0
    for i in range(len(table) + 1):
        table.insert(index, row_separator_array)
        index += 2

    # алгоритм для вывода таблицы истинности в консоль
    for i in range(len(table)):
        for j in range(len(table[i])):
            if i % 2 == 0:
                print(table[i][j], end="")
            else:
                if j == len(table[i]) - 1:
                    print(column_separator + str(table[i][j]) + column_separator, end="")
                else:
                    print(column_separator + str(table[i][j]), end="")

        print()


def generate_sdnf(arguments, function):
    sdnf = ""
    table = generate_table(arguments, function)

    for i in range(1, len(table)):
        if table[i][len(table[i]) - 1] == 1:
            term = "("
            for j in range(len(table[i]) - 1):
                if table[i][j] == 1:
                    term += str(table[0][j]) + " * "
                else:
                    term += "-" + str(table[0][j]) + " * "
            sdnf += term[:-3] + ") + "
    sdnf = sdnf[:-3]
    return sdnf


def generate_table(arguments, function):
    names = []
    for i in range(len(arguments)):
        names.append(arguments[i])
    names.append("F")

    table = [[0] * (len(arguments) + 1) for i in range(2 ** len(arguments))]
    counter = 2 ** len(arguments) / 2
    now = 0
    for i in range(len(arguments)):
        for j in range(len(table)):
            if now >= 2 * counter:
                now = 0
            if now >= counter:
                table[j][i] = 1
            now += 1
        counter /= 2
        now = 0

    for i in range(len(table)):
        list_of_arguments = []
        for j in range(len(table[i]) - 1):
            list_of_arguments.append(table[i][j])
        table[i][len(arguments)] = 1 if function(*list_of_arguments) else 0

    table.insert(0, names)

    return table


def generate_simplified_sdnf(arguments, function):
    sdnf = generate_sdnf(arguments, function)
    terms = sdnf.split(" + ")
    print(terms)
    for i in range(len(terms) - 1):
        args = terms[i][1:-1].split(" * ")
        print(args)


hack(f)
