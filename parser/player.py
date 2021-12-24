import core
import os
import json


class Player:
    Nick = "-"
    Name = "-"
    Born = "-"
    Country = "-"
    Winnings = "-"
    Years_Active_Start = "-"
    Years_Active_End = "-"


def born_to_date(born):
    [day_month, years] = born.split(",", 1)

    [month, day] = day_month.split(" ", 1)

    years = years.split("(", 1)

    year = years[0].strip()

    return year + "-" + str(core.month_string_to_number(month)) + "-" + day


def years_active_to_two_date(years_active):
    try:
        [start, end] = years_active.split("–", 1)
    except:
        [start, end] = years_active.split("-", 1)
    start = start.strip()
    end = end.strip()
    if end == "Present":
        end = "-"
    return [start, end]


def cs_check_attrs(attrs):
    tmp = Player()

    for attr in attrs:
        attr_name = attr.text
        if attr_name == "Name:":
            tmp.Name = attr.find_next('div', {'class': 'infobox-cell-2'}).text
        elif attr_name == "Nationality:" or attr_name == "Nationalities:":
            tmp.Country = core.get_country(attr.find_next('div', {'class': 'infobox-cell-2'}))
        elif attr_name == "Approx. Total Winnings:":
            tmp.Winnings = core.get_money(attr.find_next('div', {'class': 'infobox-cell-2'}).text)
        elif attr_name == "Born:":
            tmp.Born = attr.find_next('div', {'class': 'infobox-cell-2'}).find('span', {'class': 'bday'}).text
        elif attr_name == "Years Active (Player):":
            years_active = attr.find_next('div', {'class': 'infobox-cell-2'}).text
            [tmp.Years_Active_Start, tmp.Years_Active_End] = years_active_to_two_date(years_active)

    return tmp


def dota2_check_attrs(attrs):
    tmp = Player()

    for attr in attrs:
        attr_name = attr.text
        if attr_name == "Name:":
            tmp.Name = attr.find_next('div', {'class': 'infobox-cell-2'}).text
        elif attr_name == "Country:" or attr_name == "Countries:":
            tmp.Country = core.get_country(attr.find_next('div', {'class': 'infobox-cell-2'}))
        elif attr_name == "Approx. Total Earnings:":
            tmp.Winnings = core.get_money(attr.find_next('div', {'class': 'infobox-cell-2'}).text)
        elif attr_name == "Birth:":
            tmp.Born = attr.find_next('div', {'class': 'infobox-cell-2'}).find('span', {'class': 'bday'}).text

    return tmp


def lol_check_attrs(attrs):
    tmp = Player()

    for attr in attrs:
        attr_name = attr.text
        if attr_name == "Name:":
            tmp.Name = attr.find_next('div', {'class': 'infobox-cell-2'}).text
        elif attr_name == "Country:" or attr_name == "Countries:":
            tmp.Country = core.get_country(attr.find_next('div', {'class': 'infobox-cell-2'}))
        elif attr_name == "Approx. Total Earnings:":
            tmp.Winnings = core.get_money(attr.find_next('div', {'class': 'infobox-cell-2'}).text)
        elif attr_name == "Birth:":
            tmp.Born = attr.find_next('div', {'class': 'infobox-cell-2'}).find('span', {'class': 'bday'}).text
        elif attr_name == "Years Active (Player):":
            years_active = attr.find_next('div', {'class': 'infobox-cell-2'}).text
            [tmp.Years_Active_Start, tmp.Years_Active_End] = years_active_to_two_date(years_active)

    return tmp


def val_check_attrs(attrs):
    tmp = Player()

    for attr in attrs:
        attr_name = attr.text
        if attr_name == "Name:":
            tmp.Name = attr.find_next('div', {'class': 'infobox-cell-2'}).text
        elif attr_name == "Country:" or attr_name == "Countries:":
            tmp.Country = core.get_country(attr.find_next('div', {'class': 'infobox-cell-2'}))
        elif attr_name == "Approx. Total Earnings:":
            tmp.Winnings = core.get_money(attr.find_next('div', {'class': 'infobox-cell-2'}).text)
        elif attr_name == "Born:":
            tmp.Born = attr.find_next('div', {'class': 'infobox-cell-2'}).find('span', {'class': 'bday'}).text
        elif attr_name == "Years Active (Player):":
            years_active = attr.find_next('div', {'class': 'infobox-cell-2'}).text
            [tmp.Years_Active_Start, tmp.Years_Active_End] = years_active_to_two_date(years_active)

    return tmp


def game_player_get_attr(infobox, table, game_method, name_colum = 5):

    nick_id = infobox.find('div', {'class': 'infobox-header'})

    nick_id.span.decompose()

    nick = nick_id.text.strip()

    attrs = infobox.find_all('div', {'class': 'infobox-cell-2 infobox-description'})

    tmp = game_method(attrs)

    tmp.Nick = nick


    if tmp.Years_Active_Start == '-':
        try:
            history = infobox.find_all('div', {'class': 'th-mono'})
            team_one = history[0]
            team_last = history[-1]
        except:
            history = infobox.find_all('td', {'class': 'th-mono'})
            team_one = history[0]
            team_last = history[-1]


        years_first = team_one.text.split('—')[0].strip()
        years_end = team_last.text.split('—')[1].strip()

        tmp.Years_Active_Start = years_first.split('-')[0]

        if years_end == "Present":
            tmp.Years_Active_End = "-"
        else:
            tmp.Years_Active_End = years_end.split('-')[0]

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
                name_tour = attr.find('a').text.strip().replace(u'\xa0', ' ')
            elif i == (lenght - 1):
                attr.span.decompose()
                place = attr.text.strip().replace(u'\xa0', ' ')
            elif i == lenght:
                date = attr.text.strip().replace(u'\xa0', ' ')
            i += 1
        else:
            tmp_tour = {
                'name': name_tour,
                'date': date,
                'place': place
            }
            tours.append(tmp_tour)

    player_dict = {
        'nick': tmp.Nick,
        'name': tmp.Name,
        'country': tmp.Country,
        'winnings': tmp.Winnings,
        'born': tmp.Born,
        'year_active_start': tmp.Years_Active_Start,
        'year_active_end': tmp.Years_Active_End,
        'tournaments': tours
    }
    return player_dict


def cs_player_get_attr(infobox, table):
    return game_player_get_attr(infobox, table, cs_check_attrs)


def dota2_player_get_attr(infobox, table):
    return game_player_get_attr(infobox, table, dota2_check_attrs)


def val_player_get_attr(infobox, table):
    return game_player_get_attr(infobox, table, val_check_attrs)


def lol_player_get_attr(infobox, table):
    return game_player_get_attr(infobox, table, lol_check_attrs, 6)