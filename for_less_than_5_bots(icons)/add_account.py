import json
from os import mkdir
from os.path import join

from terminal import prompt


def add_new_account():
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
                     'Далее следуйте инструкциям. Остальные способы можете узнать отсюда - '
                     'http://steamcommunity.com/sharedfiles/filedetails/?id=678365301'
                     '\n\nВведите ваш SteamID(64)')
    shared_secret = prompt('Введите ваш shared_secret')
    identity_secret = prompt('Введите ваш identity_secret')

    data = {
        'username': username,
        'password': password,
        'api_key': api_key,
        'steamid': steamid,
        'shared_secret': shared_secret,
        'identity_secret': identity_secret
    }

    create_steam_guard_file(username, data)


def create_steam_guard_file(account_name, data):
    try:
        mkdir('accounts_data')
        create_steam_guard_file(account_name, data)

    except FileExistsError:
        with open(join('accounts_data', account_name + '.json'), 'w') as guard_file:
            json.dump(data, guard_file, sort_keys=True, indent=4, ensure_ascii=False)