# -*- coding: utf-8 -*-

import time
from click import prompt

from steampy.client import SteamClient, TradeOfferState


def accept_incoming_offers(username, password, api_key, steamguard_path):
    print('Запуск бота, принимающего входящие офферы')
    client = SteamClient(api_key)
    client.login(username, password, steamguard_path)
    print('Вход в Steam прошёл успешно.')
    print('Офферы будут подтверждаться каждые 10 секунд. Нажмите Ctrl+С, чтобы сделать паузу. Затем можно будет'
          ' выйти из цикла.')
    accept_offers_loop(client)


def accept_offers_loop(client):
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
        user_answer = prompt('Введите "c" на английском для продолжения')
        if (user_answer == 'c') or (user_answer == 'с'):
            print('Перезапуск подтверждения офферов. Нажмите Ctrl+С, чтобы сделать паузу.')
            accept_offers_loop(client)
        else:
            exit()


def is_donation(offer: dict):
    return offer.get('items_to_receive') \
           and not offer.get('items_to_give') \
           and offer['trade_offer_state'] == TradeOfferState.Active \
           and not offer['is_our_offer']
