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
    [start, end] = years_active.split("–", 1)
    start = start.strip()
    end = end.strip()
    if end == "Present":
        end = "-"
    return [start, end]


def cs_player_get_attr(infobox, table):
    tmp = Player()

    nick_id = infobox.find('div', {'class': 'infobox-header'})

    nick_id.span.decompose()

    tmp.Nick = nick_id.text.strip()

    attrs = infobox.find_all('div', {'class': 'infobox-cell-2 infobox-description'})

    for attr in attrs:
        attr_name = attr.text
        if attr_name == "Name:":
            tmp.Name = attr.find_next('div', {'class': 'infobox-cell-2'}).text
        elif attr_name == "Nationality:":
            tmp.Country = attr.find_next('div', {'class': 'infobox-cell-2'}).text
        elif attr_name == "Approx. Total Winnings:":
            tmp.Winnings = attr.find_next('div', {'class': 'infobox-cell-2'}).text
        elif attr_name == "Born:":
            tmp.Born = born_to_date(attr.find_next('div', {'class': 'infobox-cell-2'}).text)
        elif attr_name == "Years Active (Player):":
            years_active = attr.find_next('div', {'class': 'infobox-cell-2'}).text
            [tmp.Years_Active_Start, tmp.Years_Active_End] = years_active_to_two_date(years_active)

    table_rows = table.find_all('tr')

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


if __name__ == "__main__":
    url = "https://liquipedia.net/counterstrike/Category:Players"

    save_dir = os.getcwd() + "\\Players\\counterstrike\\"

    # core.download_category_pages(url, save_dir)
    player = core.get_item_info("https://liquipedia.net/counterstrike/S1mple", True, cs_player_get_attr)
    #player = core.get_item_info(save_dir + "1mpala.html", True, cs_player_get_attr)

    # print(born_to_date("October 2, 1997 (age 24)"))

    #core.get_game_info("counterstrike", cs_player_get_attr, True, url, save_dir, 'counterstrike_player.json')
    #tours = core.get_item_results("https://liquipedia.net/counterstrike/S1mple/Results")
    #player['torunaments'] = tours
    print(player)
    with open("player.json", 'w', encoding='utf8') as file:
        json.dump(player, file, indent=2, ensure_ascii=False)