# Парсер
import os
import shutil
import core
import player
import team
import tournament


class Game_Data:
    name = ""
    player_url = ""
    team_url = ""
    tournament_urls = ""
    get_player_method = None
    get_team_method = None
    get_tournament_method = None


def create_game_folders(save_dir):
    tmp_dir = save_dir + "\\tmp"
    player_dir = tmp_dir + "\\players"
    tournament_dir = tmp_dir + "\\tournaments"
    team_dir = tmp_dir + "\\teams"
    player_dir_res = player_dir + "_result"
    tournament_dir_res = tournament_dir + "_result"
    team_dir_res = team_dir + "_result"

    if os.path.exists(save_dir):
        shutil.rmtree(save_dir)

    os.mkdir(save_dir)
    os.mkdir(tmp_dir)
    os.mkdir(player_dir)
    os.mkdir(tournament_dir)
    os.mkdir(team_dir)
    os.mkdir(player_dir_res)
    os.mkdir(tournament_dir_res)
    os.mkdir(team_dir_res)


def game_parse(path: str, game: Game_Data, download_from_net: bool):
    save_dir = path + "\\" + game.name
    tmp_dir = save_dir + "\\tmp"
    player_dir = tmp_dir + "\\players"
    tournament_dir = tmp_dir + "\\tournaments"
    team_dir = tmp_dir + "\\teams"

    if download_from_net:
        create_game_folders(save_dir)

    core.get_game_info(game.name, game.get_player_method, download_from_net, game.player_url, player_dir,
                       save_dir + "\\" + game.name + "_players.json", 1)
    core.get_game_info(game.name, game.get_team_method, download_from_net, game.team_url, team_dir,
                      save_dir + "\\" + game.name + "_teams.json", 1)
    core.get_game_info(game.name, game.get_tournament_method, download_from_net, game.tournament_urls, tournament_dir,
                       save_dir + "\\" + game.name + "_tournament.json", 2)


def start_parse(path: str, download_from_net):
    cs_game = Game_Data()
    cs_game.name = "counterstrike"
    cs_game.player_url = "https://liquipedia.net/counterstrike/Category:Players"
    cs_game.team_url = "https://liquipedia.net/counterstrike/Category:Teams"
    cs_game.tournament_urls = [
        "https://liquipedia.net/counterstrike/Category:A-Tier_Tournaments",
        "https://liquipedia.net/counterstrike/Category:B-Tier_Tournaments",
        "https://liquipedia.net/counterstrike/Category:C-Tier_Tournaments",
        "https://liquipedia.net/counterstrike/Category:S-Tier_Tournaments",
    ]
    cs_game.get_player_method = player.cs_player_get_attr
    cs_game.get_team_method = team.cs_team_get_attr
    cs_game.get_tournament_method = tournament.cs_tour_get_attr

    game_parse(path, cs_game, download_from_net)


if __name__ == "__main__":
    start_parse(os.getcwd(), True)
