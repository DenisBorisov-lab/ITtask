def f(a, b, c):
    return a and (b or c)


def hack(function):
    arguments = function.__code__.co_varnames
    print("Таблица истинности: ")
    generate_truth_table(arguments, function)
    print()
    print("Совершенная дизъюнктивная нормальная функция: ")
    generate_sdnf(arguments, function)


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
    print(sdnf)


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
        table[i][len(arguments)] = function(*list_of_arguments)

    table.insert(0, names)

    return table


hack(f)
