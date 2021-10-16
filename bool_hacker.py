def f(a, b, c):
    return a and (b or c)


def logic1(a, b, c):
    return a and b and c or a and b and not c


def medium5(a, b, c, d, e, f): return (a and not b and not d) and (not f or e or not c and f) or (
        a and not b and not c and d) or (a and not b and c and d) or (c and not d and e and f) and (c or not e)


def logic2(a, b, c):
    return (not a or b) and not (a or b) and (not a or c)


def wiki2(x1, x2, x3, x4):
    return (not x1 and not x2 and not x3) or (x1 and x2 and x3) or (not x1 and x3 and not x4)


def medium2(a, b, c, d, e):
    return a and b or (b and not a) or (c and e) or (not c and e) or (c and not e) or (not c and not e)


def medium3(a, b, c, d, e):
    return (a and b) and (b and not a) or (c and e) and (not c and e) or (c and not e) or (not c and not e)


def simple3(a, b, c, d):
    return a and b or not c and d


def wiki1(x1, x2, x3):
    return x2 and not x3 or x1


def wiki3(x, y, z, t):
    return (y and not z and not t) or (x and not y) or (x and z)


def hack(function):
    arguments = function.__code__.co_varnames
    print("Таблица истинности: ")
    generate_truth_table(arguments, function)
    print()
    print("Совершенная дизъюнктивная нормальная функция: ")
    print(generate_sdnf(arguments, function))
    print()
    print("Упрощённая сднф: ")
    dnf = generate_simplified_sdnf(arguments, function)
    decorate_simplified_sdnf(dnf)
    print("Функция Шеффера")
    Sheffer_transformation(dnf)


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


def reduce_same_implicants(implicants):
    result = []
    for i in range(len(implicants)):
        if not (implicants[i] in result):
            result.append(implicants[i])
    return result


def difference(array1, array2) -> bool:
    count = 0
    for i in range(len(array1)):
        if array1[i] != array2[i]:
            count += 1
        if count > 1:
            return False
    return True


def glue_process(array1, array2):
    result = []
    for i in range(len(array1)):
        if array1[i] == array2[i] or array2[i] == "-" or array1[i] == "-":
            result.append(array1[i])
        else:
            result.append("-")
    return result


def glue(letters) -> list:
    new_letters = []
    for i in range(len(letters)):
        counter = 0
        for j in range(len(letters)):
            if i == j:
                continue
            elif difference(letters[i], letters[j]) and i != j:
                if not (glue_process(letters[i], letters[j]) in new_letters):
                    new_letters.append(glue_process(letters[i], letters[j]))
                counter += 1

        if counter == 0:
            new_letters.append([item.copy() for item in letters][i])
            new_letters[len(new_letters) - 1].append("*")
    return new_letters


def containsKey(array1, array2):
    counter = 0
    for i in range(len(array1)):
        if array1[i] == array2[i] or array2[i] == "-" or array1[i] == "-":
            counter += 1
    return True if counter == len(array1) else False


def isEmpty(array):
    counter = 0
    for i in range(len(array)):
        for j in range(len(array[i])):
            if (array[i][j] == "-"):
                counter += 1
    return True if counter == len(array[0]) else False


def construct_argument(str1, str2):
    result = ""
    str = str1 + str2
    for i in range(len(str)):
        if not str[i:i + 1] in result:
            result += str[i:i + 1]
    return result


def petrick(first, second):
    result = []
    second = list(second)
    for i in range(len(first)):
        for j in range(len(second)):
            if not construct_argument(first[i], second[j]) in result:
                result.append(construct_argument(first[i], second[j]))
    return result


def generate_simplified_sdnf(arguments, function):
    sdnf = generate_sdnf(arguments, function)
    terms = sdnf.split(" + ")
    letters = []
    for i in range(len(terms)):
        terms[i] = terms[i][1:-1]
        letters.append(terms[i].split(" * "))

    for i in range(len(letters)):
        for j in range(len(letters[i])):
            if letters[i][j][0:1] == "-":
                letters[i][j] = "0"
            else:
                letters[i][j] = "1"
    counter = 0
    dlc = []
    old_letters = letters
    while counter != len(letters):
        counter = 0
        letters = glue(letters)
        for i in range(len(letters)):
            if letters[i][len(letters[i]) - 1] == "*":
                counter += 1

        if counter != len(letters) and counter > 0:
            new_letter = []
            for i in range(len(letters)):
                if letters[i][len(letters[i]) - 1] != "*":
                    new_letter.append(letters[i])
                else:
                    dlc.append(letters[i])
            letters = new_letter
            if len(letters) == 1:
                letters[0].append("*")
                break

    for i in range(len(dlc)):
        letters.append(dlc[i])

    for i in range(len(letters)):
        letters[i].remove("*")

    if len(letters) == 1 and isEmpty(letters):
        return [[1]]

    table = [[0] * (len(old_letters)) for i in range(len(letters))]
    for i in range(len(letters)):
        for j in range(len(old_letters)):
            if containsKey(letters[i], old_letters[j]):
                table[i][j] = 1

    implicants = []
    if len(table) >= 1:
        for i in range(len(table[i])):
            term = ""
            for j in range(len(table)):
                if table[j][i] == 1:
                    term += str(j)
            if len(term) >= 1:
                implicants.append(term)
    i = 0
    while len(implicants) > 1:
        if i == 0:
            implicants[0] = list(implicants[0])
        implicants[0] = petrick(implicants[0], implicants[1])
        del implicants[1]
        i += 1
    min_length = 1000
    index = 0
    for i in range(len(implicants[0])):
        if len(implicants[0][i]) < min_length:
            index = i
            min_length = len(implicants[0][i])
    answer = implicants[0][index]
    result = []
    for i in range(len(answer)):
        result.append(letters[int(answer[i:i + 1])])

    for i in range(len(result)):
        term = []
        for j in range(len(result[i])):
            if result[i][j] == "1":
                term.append(arguments[j])
            elif result[i][j] == "0":
                term.append("-" + arguments[j])
        result[i] = term
    return result


def decorate_simplified_sdnf(dnf):
    result = ""
    if len(dnf) == 1 and len(dnf[0]) == 1 and dnf[0][0] == 1:
        print(1)
    else:
        for i in range(len(dnf)):
            term = ""
            for j in range(len(dnf[i])):
                term += dnf[i][j] + "*"
            result += "(" + term[:-1] + ") + "
        print(result[:-3])


# отрицвание с помощью штирха шеффера a|a = -a
def negation(simplified_sdnf):
    for i in range(len(simplified_sdnf)):
        for j in range(len(simplified_sdnf[i])):
            letter = simplified_sdnf[i][j]
            if letter[0:1] == "-":
                simplified_sdnf[i][j] = letter[1:2] + "|" + letter[1:2]
    return simplified_sdnf


# коньюкция с помощью штриха Шеффера (a|b) | (a|b) = a*b
def conjunction(simplified_sdnf):
    result_array = []
    for i in range(len(simplified_sdnf)):
        result = simplified_sdnf[i][0]
        for j in range(1, len(simplified_sdnf[i])):
            result = "(" + result + ")" if len(result) > 1 else result
            another_letter = "(" + simplified_sdnf[i][j] + ")" if len(simplified_sdnf[i][j]) > 1 else \
                simplified_sdnf[i][j]
            result = "(" + result + " | " + another_letter + ")" + " | " + "(" + result + " | " + another_letter + ")"
            result_array.append(result)
    if len(result_array) == 0 and len(simplified_sdnf) != 0:
        result_array.append(simplified_sdnf[0][0])
    return result_array


# дизъюнкция с помощью штриха Шеффера (a|a) | (a|b) = a+b
def disjunction(simplified_sdnf):
    result = simplified_sdnf[0]
    if len(simplified_sdnf) > 1:
        for i in range(1, len(simplified_sdnf)):
            result = "(" + result + ")" if len(result) > 1 else result
            another_letter = "(" + simplified_sdnf[i] + ")" if len(simplified_sdnf[i]) > 1 else simplified_sdnf[i]
            result = "(" + result + " | " + result + ")" + " | " + "(" + another_letter + " | " + another_letter + ")"
    return result


def Sheffer_transformation(dnf):
    simplified_sdnf = dnf
    if len(simplified_sdnf) == 1 and len(simplified_sdnf[0]) == 1 and simplified_sdnf[0][0] == 1:
        print(1)
    else:
        simplified_sdnf = conjunction(negation(simplified_sdnf))
        print(disjunction(simplified_sdnf))


hack(wiki3)
