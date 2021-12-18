import re

import requests
from bs4 import BeautifulSoup
import json
import os


def get_item_info(player_link, net_mode, get_method):
    if net_mode:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
        }
        r = requests.get(player_link, headers=headers).text
        soup = BeautifulSoup(r, features='html.parser')
    else:
        with open(player_link, encoding='utf8') as fp:
            soup = BeautifulSoup(fp, 'html.parser')

    infobox = soup.find('div', {'class': 'fo-nttax-infobox-wrapper'})

    return get_method(infobox)


def download_category_pages(start_url_category, folder_name):
    url_main = "https://liquipedia.net"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    }

    url_category = start_url_category

    while True:
        page = requests.get(url_category, headers=headers).text

        soup = BeautifulSoup(page, features='html.parser')

        item_category = soup.find('div', {'id': 'mw-pages'})

        item_lists = item_category.find_all('div', {'class': 'mw-category-group'})

        for player_list in item_lists:
            items = player_list.find_all('a')
            for item in items:

                if re.search(r'[:/\\*?\"<>|"]', item.text) is not None or item.text == "Banned players":
                    continue

                link = url_main + item['href']

                page = requests.get(link, headers=headers).text

                file_name = folder_name + item.text + ".html"

                print(file_name)

                with open(file_name, 'wb') as output_file:
                    output_file.write(page.encode('utf8'))

        next_page = item_category.find('a')

        i = 1

        flag = True

        while True:
            if next_page.text == "next page":
                break
            else:
                next_page = next_page.find_next('a')
            if i == 2:
                flag = False
                break
            else:
                i += 1

        if flag:
            url_category = url_main + next_page['href']
        else:
            break


def get_game_info(game, get_method, net_mode, input_path, save_path, output_path):
    if net_mode:
        download_category_pages(input_path, save_path)

    players = []

    for file in os.listdir(save_path):
        temp = get_item_info(save_path + file, False, get_method)
        players.append(temp)

    with open(output_path, 'w', encoding='utf8') as file:
        json.dump(players, file, indent=2, ensure_ascii=False)
