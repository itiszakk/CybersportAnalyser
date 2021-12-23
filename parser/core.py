import re

import requests
from bs4 import BeautifulSoup
import json
import os
from time import monotonic

start_time = 0
headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    }


def wait_2_second():
    while True:
        if monotonic() - start_time > 2:
            return


def write_json(file_path, data_to_write):
    try:
        data = json.load(open(file_path))
    except:
        data = []

    data.append(data_to_write)

    with open(file_path, "w", encoding='utf8') as fp:
        json.dump(data, fp, indent=2, ensure_ascii=False)


def month_string_to_number(string):
    m = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr': 4,
        'may': 5,
        'jun': 6,
        'jul': 7,
        'aug': 8,
        'sep': 9,
        'oct': 10,
        'nov': 11,
        'dec': 12
    }
    s = string.strip()[:3].lower()

    try:
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')


def get_item_results(result_page_link):
    global start_time
    wait_2_second()
    r = requests.get(result_page_link, headers=headers).text
    start_time = monotonic()
    soup = BeautifulSoup(r, 'html.parser')
    result_table_body = soup.find('table', {'class': 'wikitable'}).find('tbody')
    table_rows = result_table_body.find_all('tr')

    tours = []

    for i in range(1, len(table_rows)):
        if table_rows[i].get('class') is not None:
            continue
        attrs = table_rows[i].find_all('td')

        i = 1
        lenght = len(attrs)
        name_tour = '-'
        place = '-'
        date = '-'

        for attr in reversed(attrs):
            if i == 1:
                prize = attr.text.strip()
                if prize == "" or prize == "$0":
                    break
            elif i == 5:
                name_tour = attr.find('a').text.strip().replace(u'\xa0', ' ')
            elif i == (lenght - 1):
                attr.span.decompose()
                place = attr.text.strip()
            elif i == lenght:
                date = attr.text.strip()
            i += 1
        else:
            tmp = {
                'name': name_tour,
                'date': date,
                'place': place
            }
            tours.append(tmp)
    return tours


def get_item_info(save_dir, item_path, net_mode, get_method, method):
    global start_time
    if net_mode:
        wait_2_second()
        r_p = requests.get(item_path, headers=headers).text
        start_time = monotonic()
        soup_p = BeautifulSoup(r_p, features='html.parser')
        if method == 1:
            wait_2_second()
            r_r = requests.get(item_path + "/Results", headers=headers).text
            start_time = monotonic()
            soup_r = BeautifulSoup(r_r, features='html.parser')
    else:
        with open(save_dir + "\\" + item_path, encoding='utf8') as fp:
            soup_p = BeautifulSoup(fp, 'html.parser')

        if method == 1:
            with open(save_dir + "_result\\" + item_path, encoding='utf8') as fp:
                soup_r = BeautifulSoup(fp, 'html.parser')

    infobox = soup_p.find('div', {'class': 'fo-nttax-infobox-wrapper'})

    if infobox is None:
        return None
    if method == 1:
        table = soup_r.find('table', {'class': 'wikitable'}).find('tbody')
        return get_method(infobox, table)
    else:
        return get_method(infobox, None)


def download_category_pages(start_url_category, folder_name, method):
    global start_time

    url_main = "https://liquipedia.net"

    url_category = start_url_category

    while True:
        wait_2_second()
        page = requests.get(url_category, headers=headers).text
        start_time = monotonic()
        soup = BeautifulSoup(page, features='html.parser')

        item_category = soup.find('div', {'id': 'mw-pages'})
        item_lists = item_category.find_all('div', {'class': 'mw-category-group'})

        for player_list in item_lists:
            items = player_list.find_all('a')
            for item in items:
                print(item.text)
                if re.search(r'[:\\*?<>|"]', item.text) is not None or item.text == "Banned players":
                    continue

                link = url_main + item['href']
                wait_2_second()
                page = requests.get(link, headers=headers).text
                start_time = monotonic()
                file_name = folder_name + "\\" + item.text.replace("/", "_") + ".html"

                with open(file_name, 'wb') as output_file:
                    output_file.write(page.encode('utf8'))

                if method == 1:
                    link_res = link + "/Results"
                    wait_2_second()
                    page_res = requests.get(link_res, headers=headers).text
                    start_time = monotonic()
                    file_name_res = folder_name + "_result\\" + item.text.replace("/", "_") + ".html"

                    with open(file_name_res, 'wb') as output_file:
                        output_file.write(page_res.encode('utf8'))

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


def get_game_info(game, get_method, net_mode, input_path, save_path, output_path, method=1):
    print("download:" + game)
    if net_mode:
        if isinstance(input_path, str):
            download_category_pages(input_path, save_path, method)
        else:
            for path in input_path:
                download_category_pages(path, save_path, method)

    items = []
    print("parse:" + game)
    for file in os.listdir(save_path):
        print(save_path + "\\" + file)
        temp = get_item_info(save_path, file, False, get_method, method)
        items.append(temp)

    write_json(output_path, items)
