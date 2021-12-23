import core
import os
import json


class Team:
    Name = "-"
    Winnings = "-"
    Country = "-"


def cs_team_get_attr(infobox, table):
    tmp = Team()

    name_id = infobox.find('div', {'class': 'infobox-header'})

    name_id.span.decompose()

    tmp.Name = name_id.text.strip()

    attrs = infobox.find_all('div', {'class': 'infobox-cell-2 infobox-description'})

    for attr in attrs:
        attr_name = attr.text
        if attr_name == "Location:":
            country = attr.find_next('div', {'class': 'infobox-cell-2'}).text
            country = country.strip().split(" ", 1)[0]
            tmp.Country = country
        elif attr_name == "Total Winnings:":
            tmp.Winnings = attr.find_next('div', {'class': 'infobox-cell-2'}).text

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
            elif i == 4:
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


if __name__ == "__main__":
    url = "https://liquipedia.net/counterstrike/Category:Teams"

    save_dir = os.getcwd() + "\\Teams\\counterstrike\\"

    # core.download_category_pages(url, save_dir)
    temp = core.get_item_info("https://liquipedia.net/counterstrike/Natus_Vincere", True, cs_team_get_attr)

    print(temp)
    #core.get_game_info("counterstrike", cs_team_get_attr, False, url, save_dir, 'counterstrike_team.json')

    with open("team.json", 'w', encoding='utf8') as file:
        json.dump(temp, file, indent=2, ensure_ascii=False)