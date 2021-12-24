import core
import os


class Tournament:
    Name = "-"
    Date = "-"
    Winnings = "-"
    Type = "-"
    Country = "-"


def cs_check_attrs(attrs):
    tmp = Tournament()

    for attr in attrs:
        attr_name = attr.text
        if attr_name == "Type:":
            tmp.Type = attr.find_next('div', {'class': 'infobox-cell-2'}).text
        elif attr_name == "Location:":
            locations = attr.find_next('div', {'class': 'infobox-cell-2'}).text.strip()
            tmp.Country = locations.split(u'\xa0')
        elif attr_name == "Prize Pool:":
            tmp.Winnings = core.get_money(attr.find_next('div', {'class': 'infobox-cell-2'}).text)
        elif attr_name == "Start Date:":
            tmp.Date = attr.find_next('div', {'class': 'infobox-cell-2'}).text

    return tmp


def dota2_check_attrs(attrs):
    tmp = Tournament()

    for attr in attrs:
        attr_name = attr.text
        if attr_name == "Type:":
            tmp.Type = attr.find_next('div', {'class': 'infobox-cell-2'}).text
        elif attr_name == "Location:":
            locations = attr.find_next('div', {'class': 'infobox-cell-2'}).text.strip()
            tmp.Country = locations.split(u'\xa0')
        elif attr_name == "Prize Pool:":
            tmp.Winnings = core.get_money(attr.find_next('div', {'class': 'infobox-cell-2'}).text)
        elif attr_name == "Start Date:":
            tmp.Date = attr.find_next('div', {'class': 'infobox-cell-2'}).text

    return tmp


def val_check_attrs(attrs):
    tmp = Tournament()

    for attr in attrs:
        attr_name = attr.text
        if attr_name == "Type:":
            tmp.Type = attr.find_next('div', {'class': 'infobox-cell-2'}).text
        elif attr_name == "Location:":
            locations = attr.find_next('div', {'class': 'infobox-cell-2'}).text.strip()
            tmp.Country = locations.split(u'\xa0')
        elif attr_name == "Prize Pool:":
            tmp.Winnings = core.get_money(attr.find_next('div', {'class': 'infobox-cell-2'}).text)
        elif attr_name == "Start Date:":
            tmp.Date = attr.find_next('div', {'class': 'infobox-cell-2'}).text

    return tmp


def lol_check_attrs(attrs):
    tmp = Tournament()

    for attr in attrs:
        attr_name = attr.text
        if attr_name == "Type:":
            tmp.Type = attr.find_next('div', {'class': 'infobox-cell-2'}).text
        elif attr_name == "Location:":
            locations = attr.find_next('div', {'class': 'infobox-cell-2'}).text.strip()
            tmp.Country = locations.split(u'\xa0')
        elif attr_name == "Prize Pool:":
            tmp.Winnings = core.get_money(attr.find_next('div', {'class': 'infobox-cell-2'}).text)
        elif attr_name == "Start Date:":
            tmp.Date = attr.find_next('div', {'class': 'infobox-cell-2'}).text

    return tmp


def game_tour_get_attr(infobox, table, game_method):
    name_id = infobox.find('div', {'class': 'infobox-header'})

    name_id.span.decompose()

    name = name_id.text.strip().replace(u'\xa0', ' ')

    attrs = infobox.find_all('div', {'class': 'infobox-cell-2 infobox-description'})

    tmp = game_method(attrs)

    tmp.Name = name

    player_dict = {
        'name': tmp.Name,
        'date': tmp.Date,
        'type': tmp.Type,
        'country': tmp.Country,
        'winnings': tmp.Winnings,
    }
    return player_dict


def cs_tour_get_attr(infobox, table):
    return game_tour_get_attr(infobox, table, cs_check_attrs)


def dota2_tour_get_attr(infobox, table):
    return game_tour_get_attr(infobox, table, dota2_check_attrs)


def val_tour_get_attr(infobox, table):
    return game_tour_get_attr(infobox, table, val_check_attrs)


def lol_tour_get_attr(infobox, table):
    return game_tour_get_attr(infobox, table, lol_check_attrs)
