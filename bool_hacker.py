import time


def f(a, b, c):
    return a and (b or c)


def logic1(a, b, c):
    return a and b and c or a and b and not c


def medium5(a, b, c, d, e, f): return (a and not b and not d) and (not f or e or not c and f) or (
        a and not b and not c and d) or (a and not b and c and d) or (c and not d and e and f) and (c or not e)


def logic2(a, b, c):
    return (not a or b) and not (a or b) and (not a or c)


def medium2(a, b, c, d, e):
    return a and b or (b and not a) or (c and e) or (not c and e) or (c and not e) or (not c and not e)


def medium3(a, b, c, d, e):
    return (a and b) and (b and not a) or (c and e) and (not c and e) or (c and not e) or (not c and not e)


def simple3(a, b, c, d):
    return a and b or not c and d


def hack(function):
    arguments = function.__code__.co_varnames
    print("Таблица истинности: ")
    generate_truth_table(arguments, function)
    print()
    print("Совершенная дизъюнктивная нормальная функция: ")
    print(generate_sdnf(arguments, function))
    print()
    print("Упрощённая сднф: ")
    simplified_sdnf = generate_simplified_sdnf(arguments, function)
    decorate_simplified_sdnf(simplified_sdnf)
    print("Функция Шеффера")
    Sheffer_transformation(simplified_sdnf)


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


def is_glued(first, second) -> bool:
    count = 0
    is_the_same = False
    if len(first) != len(second):
        return False
    for i in range(len(first)):
        if first[i] in second:
            count += 1
        else:
            if first[i][0:1] == "-":
                if first[i][1:2] in second:
                    is_the_same = True
            elif first[i][0:1] != "-":
                if "-" + first[i] in second:
                    is_the_same = True
            else:
                return False
    return True if count == len(first) - 1 and is_the_same else False


def generate_term(first_array, second_array):
    result_array = []
    for i in range(len(first_array)):
        if first_array[i] == second_array[i]:
            result_array.append(first_array[i])
    return result_array


def contains_implicants(implicants, letters):
    counter = 0
    for i in range(len(implicants)):
        if implicants[i] in letters:
            counter += 1
    return True if counter == len(implicants) else False


def reduce_same_implicants(implicants):
    result = []
    for i in range(len(implicants)):
        if not (implicants[i] in result):
            result.append(implicants[i])
    return result

def isEmpty(array):
    for i in range(len(array)):
        if len(array[i]) == 0:
            return True
    return False
def generate_simplified_sdnf(arguments, function):
    sdnf = generate_sdnf(arguments, function)
    terms = sdnf.split(" + ")
    letters = []
    implicants = []
    for i in range(len(terms)):
        terms[i] = terms[i][1:-1]
        letters.append(terms[i].split(" * "))

    old_letters = letters
    global_counter = -1
    v = 0
    while global_counter != 0:
        global_counter = -1
        for i in range(len(letters)):
            glue_count = 0
            for j in range(0, len(letters)):
                if i != j:
                    if is_glued(letters[i], letters[j]):
                        global_counter += 1
                        if not generate_term(letters[i], letters[j]) in implicants:
                            implicants.append(generate_term(letters[i], letters[j]))
                        glue_count += 1

            # print("Step", str(v) + ":", implicants)
            # time.sleep(1)
            v+=1
            if glue_count == 0:
                implicants.append(letters[i])
            if len(implicants) == 0:
                break
        letters = implicants
        implicants = []
        global_counter += 1

    letters = reduce_same_implicants(letters)

    implicantion_table = [[0] * (len(old_letters)) for i in range(len(letters))]
    for i in range(len(old_letters)):
        for j in range(len(letters)):
            if contains_implicants(letters[j], old_letters[i]):
                implicantion_table[j][i] = 1

    simplified_implicants = []
    # проход по импликационной таблице
    for i in range(len(old_letters)):
        counter = 0
        position = 0
        for j in range(len(letters)):
            if implicantion_table[j][i] == 1:
                counter += 1
                position = j
        if counter == 1:
            simplified_implicants.append(letters[position])
        elif counter == 0:
            simplified_implicants.append(letters[position])

    if isEmpty(simplified_implicants):
        return [[1]]
    return reduce_same_implicants(simplified_implicants)


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


hack(f)
