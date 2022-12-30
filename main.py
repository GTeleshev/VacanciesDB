from ConnectDb import ConnectDb
from tabulate import tabulate

connect = ConnectDb()

VACVERSION = '1.0'


def get_records():
    data = connect.select_all_db()
    data.insert(0, ('ID', 'Название', 'Навыки', 'Описание', 'Зарплата', 'Тип'))
    print(tabulate(data))


def add_record():
    data = []
    data.append(input('Введите наименование вакансии: '))
    data.append(input('Введите ключевые навыки: '))
    data.append(input('Введите описание: '))
    res = False
    while not res:
        salary = input('Введите размер заработной платы: ')
        if salary.isdigit():
            data.append(float(salary))
            res = True
    res1 = False
    while not res1:
        type = input('Введите тип вакансии (1 - удаленный, 2 - смешанный, 3 - в офисе): ')
        if type.isdigit() and int(type) in range(1, 4):
            data.append(int(type))
            res1 = True
    connect.insert_in_db(data[0], data[1], data[2], data[3], data[4])


def search():
    ln = input('Введите название (целиком): ')
    column = "NAME"
    data = connect.select_where(column, ln)
    if data == []:
        print('Запись не найдена')
    else:
        data.insert(0, ('ID', 'Название', 'Навыки', 'Описание', 'Зарплата', 'Тип'))
        print(tabulate(data))


def search_partial():
    res = False
    while not res:
        ln = input('Введите название (5 символов): ')
        if len(ln) == 5:
            break
    column = "NAME"
    data = connect.select_where_like(column, ln)
    if data == []:
        print('Запись не найдена')
    else:
        data.insert(0, ('ID', 'Название', 'Навыки', 'Описание', 'Зарплата', 'Тип'))
        print(tabulate(data))


def delete_record():
    while True:
        id_ = input('Введите ID: ')
        if id_.isdigit():
            connect.delete_by_id(id_)
            break


def purge_database():
    connect.clear_db()


def exit_db():
    exit()


def check_numeric(message, min_, max_):
    out = -100
    check = False
    while not check or out > max_ or out < min_:
        str_out = input(message)
        if not str_out.isdigit():
            check = False
        else:
            out = int(str_out)
            check = True
    return out


def main_menu():
    print(f"База вакансий: {VACVERSION}")
    options = {1: "Добавление записей",
               2: "Вывод на экран",
               3: "Удаление записей",
               4: "Полнотекстовый поиск ",
               5: "Поиск (5 символов)",
               6: "Завершить работу",
               7: "Очистка базы"}
    functions = {1: add_record,
                 2: get_records,
                 3: delete_record,
                 4: search,
                 5: search_partial,
                 6: exit_db,
                 7: purge_database}
    for iter in options.keys():
        print(iter, options[iter])
    option = check_numeric("Выберите действие: ", 1, 8)
    print("Выбрано: ", options[option])
    functions[option]()  # можно передавать без аргумента "()"

    user_dec = input('Вернуться в меню - Enter, номер функции - от 1 до 7, выйти - exit: ')
    if user_dec == 'exit':
        exit_db()
    elif user_dec.isdigit() and int(user_dec) in range(1, 8):
        functions[int(user_dec)]()
    else:
        main_menu()
    return option


main_menu()