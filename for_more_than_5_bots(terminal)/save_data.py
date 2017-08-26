import json
from os import mkdir
from os.path import join

data_file_name = 'account_data.json'


# Данная функция создаёт файл, необходимый для входа в Steam через библиотеку steampy, в папке guard.
def create_steam_guard_file(account_name, steamid, shared_secret, identity_secret):
    try:
        mkdir('guard')
        create_steam_guard_file(account_name, steamid, shared_secret, identity_secret)

    except FileExistsError:
        with open(join('guard', account_name + '.json'), 'a') as guard_file:
            guard_dict = {"steamid": steamid, "shared_secret": shared_secret, "identity_secret": identity_secret}
            json.dump(guard_dict, guard_file, sort_keys=True, indent=4, ensure_ascii=False)


# Данная функция добавляет в файл данные, введённые пользователем в add_new_account().
def add_in_data(data):
    with open(data_file_name, 'w') as new_file:
        json.dump(data, new_file, sort_keys=True, indent=4, ensure_ascii=False)
        print('\nДанные сохранены!')
