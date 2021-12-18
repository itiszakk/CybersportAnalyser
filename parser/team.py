import core
import os


class Team:
    Name = "-"
    Winnings = "-"
    Country = "-"


def cs_team_get_attr(infobox):
    tmp = Team()

    name_id = infobox.find('div', {'class': 'infobox-header'})

    name_id.span.decompose()

    tmp.Name = name_id.text.replace(" ", "")

    attrs = infobox.find_all('div', {'class': 'infobox-cell-2 infobox-description'})

    for attr in attrs:
        attr_name = attr.text
        if attr_name == "Location:":
            tmp.Country = attr.find_next('div', {'class': 'infobox-cell-2'}).text
        elif attr_name == "Total Winnings:":
            tmp.Winnings = attr.find_next('div', {'class': 'infobox-cell-2'}).text

    player_dict = {
        'Name': tmp.Name,
        'Country': tmp.Country,
        'Winnings': tmp.Winnings
    }
    return player_dict


if __name__ == "__main__":
    url = "https://liquipedia.net/counterstrike/Category:Teams"

    save_dir = os.getcwd() + "\\Teams\\counterstrike\\"

    # core.download_category_pages(url, save_dir)
    # temp = get_item_info("https://liquipedia.net/counterstrike/ARCY", True, cs_team_get_attr)

    # print(temp)
    core.get_game_info("counterstrike", cs_team_get_attr, True, url, save_dir, 'counterstrike_team.json')
