import core
import os
import json


class Tournament:
    Name = "-"
    Date = "-"
    Winnings = "-"
    Type = "-"
    Country = "-"


def cs_tour_get_attr(infobox, table):
    tmp = Tournament()

    name_id = infobox.find('div', {'class': 'infobox-header'})

    name_id.span.decompose()

    tmp.Name = name_id.text.strip().split(u'\xa0')

    attrs = infobox.find_all('div', {'class': 'infobox-cell-2 infobox-description'})

    for attr in attrs:
        attr_name = attr.text
        if attr_name == "Type:":
            tmp.Type = attr.find_next('div', {'class': 'infobox-cell-2'}).text
        elif attr_name == "Location:":
            locations = attr.find_next('div', {'class': 'infobox-cell-2'}).text.strip()
            tmp.Country = locations.split(u'\xa0')
        elif attr_name == "Prize Pool:":
            tmp.Winnings = attr.find_next('div', {'class': 'infobox-cell-2'}).text.replace(u'\xa0', ' ')
        elif attr_name == "Start Date:":
            tmp.Date = attr.find_next('div', {'class': 'infobox-cell-2'}).text
    player_dict = {
        'name': tmp.Name,
        'date': tmp.Date,
        'type': tmp.Type,
        'country': tmp.Country,
        'winnings': tmp.Winnings,
    }
    return player_dict


if __name__ == "__main__":
    url = "https://liquipedia.net/counterstrike/Category:A-Tier_Tournaments"

    save_dir = os.getcwd() + "\\counterstrike\\tmp\\tours\\"

    # core.download_category_pages(url, save_dir)
    #temp = core.get_item_info("https://liquipedia.net/counterstrike/EXTREMESLAND/2021/Qualifier/Southeast_Asia", True, cs_tour_get_attr)

    # print(temp)
    core.get_game_info("counterstrike", cs_tour_get_attr, False, url, save_dir, 'counterstrike_tour.json')

    #with open("tours.json", 'w', encoding='utf8') as file:
    #    json.dump(temp, file, indent=2, ensure_ascii=False)