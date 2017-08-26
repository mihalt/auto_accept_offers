# -*- coding: utf-8 -*-

import json
import time
from os.path import join

from click import prompt
from steampy.client import SteamClient, TradeOfferState

from add_account import add_new_account

"""
ВВОД ДАННЫХ
Название файла, которое необходимо ввести ниже, генерируется автоматически, после запуска без
редактирования данного скрипта или скрипта add_account.py и ввода данных в него данных.
Найдите в папке accounts_data файл с данными, имя которого соответствует логину вашего аккаунта.

Пример вставки ниже: account_file = 'account_login.json' 
"""
account_file = 'название_файла.json'


def main():
    try:
        steamguard_path = join('accounts_data', account_file)
        with open(steamguard_path, 'r') as guard_file:
            data = json.load(guard_file)

            username = data['username']
            password = data['password']
            api_key = data['api_key']
            print('Запуск бота, принимающего входящие офферы')
            client = SteamClient(api_key)
            client.login(username, password, steamguard_path)
            print('Вход в Steam прошёл успешно.')
            print('Офферы будут подтверждаться каждые 10 секунд. Нажмите Ctrl+С, чтобы сделать паузу.')
            accept_offers(client)

    except FileNotFoundError:
        add_new_account()

    except json.decoder.JSONDecodeError:
        user_answer = prompt('\nОшибка декодирования. Скорее всего файлы с данными об аккаунтах пусты'
                             ' или введены не верно.\n'
                             'Введите add, чтобы добавить\перезаписать новый аккаунт или любые символы, '
                             'чтобы выйти из программы\n'
                             'Ввод')

        if user_answer == 'add':
            add_new_account()

        else:
            exit()


def accept_offers(client):
    if client.is_session_alive():
        try:
            while True:
                offers = client.get_trade_offers()['response']['trade_offers_received']
                for offer in offers:
                    if is_donation(offer):
                        offer_id = offer['tradeofferid']
                        num_accepted_items = len(offer['items_to_receive'])
                        client.accept_trade_offer(offer_id)
                        print('Принятые предложения {} - всего скинов в оффере {}'.format(offer_id, num_accepted_items))
                time.sleep(10)

        except KeyboardInterrupt:
            user_answer = prompt('Введите "c" для продолжения')
            if (user_answer == 'c') or (user_answer == 'с'):
                print('Перезапуск подтверждения офферов. Нажмите Ctrl+С, чтобы сделать паузу.')
                accept_offers(client)
            else:
                exit()

    else:
        main()


def is_donation(offer: dict):
    return offer.get('items_to_receive') \
           and not offer.get('items_to_give') \
           and offer['trade_offer_state'] == TradeOfferState.Active \
           and not offer['is_our_offer']


if __name__ == "__main__":
    main()
