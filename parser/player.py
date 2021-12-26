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
    try:
        [day_month, years] = born.split(',', 1)

        [month, day] = day_month.split(' ', 1)

        years = years.split('(', 1)

        year = years[0].strip()

        return year + "-" + str(core.month_string_to_number(month)) + "-" + day
    except:
        if born.strip().isdigit():
            return born.strip()
        return '-'


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
            try:
                tmp.Born = attr.find_next('div', {'class': 'infobox-cell-2'}).find('span', {'class': 'bday'}).text
            except:
                temp_div = attr.find_next('div', {'class': 'infobox-cell-2'}).text.strip()
                tmp.Born = born_to_date(temp_div)
                print(tmp.Born)
        elif attr_name == "Years Active (Player):":
            years_active = attr.find_next('div', {'class': 'infobox-cell-2'}).text
            try:
                [tmp.Years_Active_Start, tmp.Years_Active_End] = years_active_to_two_date(years_active)
            except:
                tmp.Years_Active_Start = tmp.Years_Active_End = years_active.strip()

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
            try:
                tmp.Born = attr.find_next('div', {'class': 'infobox-cell-2'}).find('span', {'class': 'bday'}).text
            except:
                temp_div = attr.find_next('div', {'class': 'infobox-cell-2'}).text.strip()
                tmp.Born = born_to_date(temp_div)
                print(tmp.Born)

    return tmp


def lol_check_attrs(attrs):
    tmp = Player()

    for attr in attrs:
        attr_name = attr.text
        if attr_name == "Name:":
            tmp.Name = attr.find_next('div', {'class': 'infobox-cell-2'}).text
        elif attr_name == "Country:" or attr_name == "Countries:":
            try:
                tmp.Country = core.get_country(attr.find_next('div', {'class': 'infobox-cell-2'}))
            except:
                tmp.Country = attr.find_next('div', {'class': 'infobox-cell-2'}).text.strip()
                print(tmp.Country)
        elif attr_name == "Approx. Total Earnings:":
            tmp.Winnings = core.get_money(attr.find_next('div', {'class': 'infobox-cell-2'}).text)
        elif attr_name == "Birth:":
            try:
                tmp.Born = attr.find_next('div', {'class': 'infobox-cell-2'}).find('span', {'class': 'bday'}).text
            except:
                temp_div = attr.find_next('div', {'class': 'infobox-cell-2'}).text.strip()
                tmp.Born = born_to_date(temp_div)
                print(tmp.Born)
        elif attr_name == "Years Active (Player):":
            years_active = attr.find_next('div', {'class': 'infobox-cell-2'}).text
            try:
                [tmp.Years_Active_Start, tmp.Years_Active_End] = years_active_to_two_date(years_active)
            except:
                tmp.Years_Active_Start = tmp.Years_Active_End = years_active.strip()

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
            try:
                tmp.Born = attr.find_next('div', {'class': 'infobox-cell-2'}).find('span', {'class': 'bday'}).text
            except:
                temp_div = attr.find_next('div', {'class': 'infobox-cell-2'}).text.strip()
                tmp.Born = born_to_date(temp_div)
                print(tmp.Born)
        elif attr_name == "Years Active (Player):":
            years_active = attr.find_next('div', {'class': 'infobox-cell-2'}).text
            try:
                [tmp.Years_Active_Start, tmp.Years_Active_End] = years_active_to_two_date(years_active)
            except:
                tmp.Years_Active_Start = tmp.Years_Active_End = years_active.strip()

    return tmp


def game_player_get_attr(infobox, table, game_method, name_colum=5):
    nick_id = infobox.find('div', {'class': 'infobox-header'})

    nick_id.span.decompose()

    nick = nick_id.text.strip()

    attrs = infobox.find_all('div', {'class': 'infobox-cell-2 infobox-description'})

    tmp = game_method(attrs)

    tmp.Nick = nick

    if tmp.Years_Active_Start == '-':
        i = 0
        history = infobox.find_all('td', {'class': 'th-mono'})
        if not history:
            history = infobox.find_all('div', {'class': 'th-mono'})
            if not history:
                print("Not history")
            else:
                try:
                    team_one = history[i]
                    team_last = history[-1]
                except:
                    team_one = history[i]
                    team_last = history[-1]

                years_first = team_one.text.split('-')[0].strip()
                while years_first.rfind('?') != -1:
                    i += 1
                    try:
                        team_one = history[i]
                    except:
                        years_first = '-'
                        break
                    years_first = team_one.text.split('-')[0].strip()

                tmp.Years_Active_Start = years_first

                team_last = team_last.text

                team_last = team_last.replace('—', '-')
                team_last = team_last.replace('–', '-')

                try:
                    years_end = team_last.split('-')[3].strip()
                except:
                    years_end = '-'

                if years_end == "Present":
                    tmp.Years_Active_End = "-"
                else:
                    tmp.Years_Active_End = years_end
                print(years_end)
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
