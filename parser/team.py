import core
import os
import json


class Team:
    Name = "-"
    Winnings = "-"
    Country = "-"


def cs_check_attrs(attrs):
    tmp = Team()

    for attr in attrs:
        attr_name = attr.text
        if attr_name == "Location:":
            tmp.Country = core.get_country(attr.find_next('div', {'class': 'infobox-cell-2'}))
        elif attr_name == "Total Winnings:":
            tmp.Winnings = core.get_money(attr.find_next('div', {'class': 'infobox-cell-2'}).text)

    return tmp


def dota2_check_attrs(attrs):
    tmp = Team()

    for attr in attrs:
        attr_name = attr.text
        if attr_name == "Location:":
            tmp.Country = core.get_country(attr.find_next('div', {'class': 'infobox-cell-2'}))
        elif attr_name == "Total Earnings:":
            tmp.Winnings = core.get_money(attr.find_next('div', {'class': 'infobox-cell-2'}).text)

    return tmp


def val_check_attrs(attrs):
    tmp = Team()

    for attr in attrs:
        attr_name = attr.text
        if attr_name == "Location:":
            tmp.Country = core.get_country(attr.find_next('div', {'class': 'infobox-cell-2'}))
        elif attr_name == "Total Winnings:":
            tmp.Winnings = core.get_money(attr.find_next('div', {'class': 'infobox-cell-2'}).text)

    return tmp


def lol_check_attrs(attrs):
    tmp = Team()

    for attr in attrs:
        attr_name = attr.text
        if attr_name == "Location:":
            tmp.Country = core.get_country(attr.find_next('div', {'class': 'infobox-cell-2'}))
        elif attr_name == "Total Earnings:":
            tmp.Winnings = core.get_money(attr.find_next('div', {'class': 'infobox-cell-2'}).text)

    return tmp


def game_team_get_attr(infobox, table, game_method, name_colum=4):

    name_id = infobox.find('div', {'class': 'infobox-header'})

    name_id.span.decompose()

    name_id.text.strip()

    name = name_id.text.strip()

    attrs = infobox.find_all('div', {'class': 'infobox-cell-2 infobox-description'})

    tmp = game_method(attrs)

    tmp.Name = name

    if table == '-':
        tours = []
    else:
        table_rows = table.find_all('tr')

        tours = []

        for i in range(1, len(table_rows)):
            if table_rows[i].get('class') is not None and table_rows[i].get('class').count('sortbottom') == 1:
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
                elif i == name_colum:
                    try:
                        name_tour = attr.find('a').text.strip().replace(u'\xa0', ' ')
                    except:
                        name_tour = attr.text.strip()
                elif i == (lenght - 1):
                    attr.span.decompose()
                    place = attr.text.strip()
                elif i == lenght:
                    date = attr.text.strip()
                i += 1
            else:
                tmp_tour = {
                    'name': name_tour,
                    'date': date,
                    'place': place,
                }
                tours.append(tmp_tour)

    player_dict = {
        'name': tmp.Name,
        'country': tmp.Country,
        'winnings': tmp.Winnings,
        'tournaments': tours
    }
    return player_dict


def cs_team_get_attr(infobox, table):
    return game_team_get_attr(infobox, table, cs_check_attrs)


def dota2_team_get_attr(infobox, table):
    return game_team_get_attr(infobox, table, dota2_check_attrs)


def val_team_get_attr(infobox, table):
    return game_team_get_attr(infobox, table, val_check_attrs)


def lol_team_get_attr(infobox, table):
    return game_team_get_attr(infobox, table, lol_check_attrs, 5)