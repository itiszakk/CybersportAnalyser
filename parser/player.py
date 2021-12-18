import core
import os


class Player:
    Nick = "-"
    Name = "-"
    Born = "-"
    Country = "-"
    Status = "-"
    Years_Active = "-"


def cs_player_get_attr(infobox):
    tmp = Player()

    nick_id = infobox.find('div', {'class': 'infobox-header'})

    nick_id.span.decompose()

    tmp.Nick = nick_id.text.replace(" ", "")

    attrs = infobox.find_all('div', {'class': 'infobox-cell-2 infobox-description'})

    for attr in attrs:
        attr_name = attr.text
        if attr_name == "Name:":
            tmp.Name = attr.find_next('div', {'class': 'infobox-cell-2'}).text
        elif attr_name == "Status:":
            tmp.Status = attr.find_next('div', {'class': 'infobox-cell-2'}).text
        elif attr_name == "Nationality:":
            tmp.Country = attr.find_next('div', {'class': 'infobox-cell-2'}).text
        elif attr_name == "Born:":
            tmp.Born = attr.find_next('div', {'class': 'infobox-cell-2'}).text
        elif attr_name == "Years Active (Player):":
            tmp.Years_Active = attr.find_next('div', {'class': 'infobox-cell-2'}).text
    player_dict = {
        'nick': tmp.Nick,
        'name': tmp.Name,
        'country': tmp.Country,
        'born': tmp.Born,
        'status': tmp.Status,
        'year_active': tmp.Years_Active
    }
    return player_dict


if __name__ == "__main__":
    url = "https://liquipedia.net/dota2/Category:Players"

    save_dir = os.getcwd() + "\\Players\\counterstrike\\"

    # download_player_pages(url, save_dir)
    # get_player_info("https://liquipedia.net/counterstrike/SOKER", True, cs_player_get_attr)

    core.get_game_info("counterstrike", cs_player_get_attr, True, url, save_dir, 'counterstrike_player.json')
