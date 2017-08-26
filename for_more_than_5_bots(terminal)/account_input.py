# -*- coding: utf-8 -*-

"""
Этот скрипт является модулем (составляющей) проограммы для торговли скинами в Steam.

Данный модуль является главным в программе. Его основная функция заключается в том,
чтобы спрашивать у пользователя, что ему необходимо и в зависимости от этого производить
такие действия (каждое действие - отдельный модуль:

1. Сохранять данные аккаунта, если их нет в системе. Они сохраняются в файл account_data.json,
 а так же создаёт папку guard и сохраняет отдельные данные, необходимые для аутендефикации и авторизации в Steam.
2. Принятие входящих трейдов в цикле и его пауза при нажатии Ctrl+C. Возобновление при вводе 'c'.
3. и т.д. Функционал будет расширяться

Программа предполагает, что у пользователя уже есть доступ к торговой площадке и возможность мгновенного обмена
"""

import json
from os.path import abspath, join
from sys import exit

from accept_offers import accept_incoming_offers
from save_data import create_steam_guard_file, add_in_data
from click import prompt


def main():
    """Главная функция, которая вызывается после запуска скрипта.

    Определяет, есть ли файл с
    базой аккаунтов - account_data.json. Так же даёт возможность пользователю
    выбрать первый аккаунт из списка, после ввода любых символов.
    """

    try:
        with open(data_file_name, 'r+') as data_file:
            global data
            data = json.load(data_file)
            string = ''
            counter = 1
            dict_bots_ids_names = {}  # Словарь в котором ключи являются цифрами (индентификаторми)

            for account_name in data:
                dict_bots_ids_names[str(counter)] = account_name
                string += '{n}: {username}\n'.format(n=counter, username=account_name)
                counter += 1

            list_bots_ids_names_values = list(dict_bots_ids_names.values())

            user_answer = prompt('\nВаши аккаунты в программе:\n' + string +
                                 '\nДобавить дополнительные аккаунты? - введите add\n'
                                 'Выбрать аккаунт, от которого хотите совершать действие - введите его номер '
                                 'или имя\n'
                                 'Совершить действие от первого аккаунта в списке - введите любой символ\n'
                                 'Выйти из программы - введите e\n'
                                 '\nВведите данные и нажмите Enter')

            if user_answer == 'add':
                add_new_account()
                main()

            elif (user_answer in list_bots_ids_names_values) or (user_answer in dict_bots_ids_names):
                choose_account_and_accept_offers(user_answer, data, dict_bots_ids_names, string)


            elif (user_answer == 'e') or (user_answer == 'е'):
                exit()


            elif not data:
                add_new_account()


            else:
                first_username = dict_bots_ids_names['1']
                accept_incoming_offers(first_username, data[first_username]['steam']['password'],
                                       data[first_username]['steam']['api_key'], abspath(join('guard', first_username)))
                repeat_user(data, dict_bots_ids_names, string)


    except FileNotFoundError:
        add_new_account()


    except json.decoder.JSONDecodeError:
        user_answer = prompt('\nОшибка декодирования. Скорее всего файлы с данными об аккаунтах пусты.\n'
                             'Введите add, чтобы добавить новый аккаунт или любые символы, чтобы выйти из программы\n'
                             'Ввод')

        if user_answer == 'add':
            add_new_account()

        else:
            exit()


def add_new_account():
    """Добавить новый аккаунт в систему

    При вызове данной функции у пользователя запрашиваются все необходимые данные для аутендификации в Steam.
    Функция возвращает словарь со всеми значениями, для её дальнейшей отправки в account_data.json.
    Так же выделяются данные необходимые для входа через библиотеку steampy и создаётся соответствующий файл
    в папке guard.
    """

    username = prompt('\nВведите ваш логин от Steam')
    password = prompt('Введите ваш пароль')
    api_key = prompt('\nВвод API-ключа Steam. Вы его можете сделать доступным, '
                     'после перехода по ссылке https://steamcommunity.com/dev/apikey. '
                     'Для того, чтобы сделать его доступным необходимо один раз запустить на аккаунте '
                     'любую игру.\n\nИтак, введите API-ключ')
    steamid = prompt('\nСледующие данные, если вы пользовались Steam Desktop Autendeficator, '
                     'можете найти в папке maFiles. Имя файла соответствует вашему SteamID(64)'
                     'Открывайте простым текстовым редактором. Если данные будут закодированы, то '
                     'просто сбросьте пароь от программы - зайдите в неё и нажмите Setup Encryption. '
                     'Далее следуйте инструкциям'
                     '\n\nВведите ваш SteamID(64)')
    shared_secret = prompt('Введите ваш shared_secret')
    identity_secret = prompt('Введите ваш identity_secret')

    data[username] = {
        'steam':
            {
                'username': username,
                'password': password,
                'api_key': api_key,
                'steamid': steamid,
                'shared_secret': shared_secret,
                'identity_secret': identity_secret
            }
    }

    create_steam_guard_file(username, steamid, shared_secret, identity_secret)
    add_in_data(data)
    main()


def choose_account_and_accept_offers(user_answer, data, dict_bots_ids_names, string):
    # Данная функция позволяет выбрать от имени какого аккаунта необходимо совершить действие и логинится

    if user_answer in map(str, dict_bots_ids_names):
        username = dict_bots_ids_names[user_answer]
        guard_file = abspath(join('guard', username + '.json'))
        accept_incoming_offers(username, data[username]['steam']['password'], data[username]['steam']['api_key'],
                               guard_file)
        repeat_user(data, dict_bots_ids_names, string)


    elif user_answer in data.keys():
        guard_file = abspath(join('guard', user_answer))
        accept_incoming_offers(user_answer, data[user_answer]['steam']['password'],
                               data[user_answer]['steam']['api_key'], guard_file)
        repeat_user(data, dict_bots_ids_names, string)

    else:
        user_answer = prompt(
            string + '\nНекорректный ввод. Введите номер бота или его имя, от которого вы хотите совершить действие')
        choose_account_and_accept_offers(user_answer, data, dict_bots_ids_names, string)


def repeat_user(data, dict_bots_ids_names, string):
    # Данная функция позволяет пользователю продолжить работу с программой, после её удачного окончания по одному аккаунту.

    user_answer = prompt('\n-Выбрать другой или этот аккаунт? - Введите номер бота или его имя \n\n' + string +
                         '\n-Добавить дополнительные аккаунты? - введите add\n'
                         '-Закрыть программу? - введите любой символ\n'
                         'Ввод данных'
                         )

    if (user_answer in data) or (user_answer in dict_bots_ids_names):
        choose_account_and_accept_offers(user_answer, data, dict_bots_ids_names, string)

    elif user_answer == 'add':
        add_new_account()


    else:
        exit()

    main()


data_file_name = abspath('account_data.json')
data = {}
main()


"""
Создано Михаилом Алтыниным
https://vk.com/mihailaltinin

Проект GameTrading.biz
https://vk.com/gametrading

© 2017 Михаил Алтынин
"""