import re
from typing import Tuple, Union

from discord import Color
from mcstatus import JavaServer
from mcstatus.pinger import PingResponse


def get_server_info(minecraft_server: str):
    try:
        return JavaServer.lookup(minecraft_server).status()
    except Exception:
        return None


def is_server_online(response: Union[PingResponse, None]):
    return hasattr(response, 'version') and re.match(r'^\d+(\.\d+){1,2}$', response.version.name)


def get_server_status(response: PingResponse) -> Tuple[str, Color]:
    return ('Online', Color.green()) if is_server_online(response) else ('Offline', Color.red())


def is_player_exists(player: PingResponse.Players.Player):
    return hasattr(player, 'name')


def get_player_name(player_data: Tuple[int, PingResponse.Players.Player]):
    idx, player = player_data
    return f'{idx + 1}. {player.name}' if is_player_exists(player) else ''


def are_players_exists(players: PingResponse.Players):
    return hasattr(players, 'sample')


def get_players_name(players: PingResponse.Players):
    return '\n'.join(map(get_player_name, enumerate(players.sample))) if are_players_exists(players) else ''


def are_there_online_players(response: Union[PingResponse, None], server_status: str):
    return hasattr(response, 'players') and server_status == 'Online'


def no_players_online(response: Union[PingResponse, None], server_status: str):
    return not (are_there_online_players(response, server_status) and are_players_exists(response.players))


def get_online_players(response: Union[PingResponse, None], server_status: str) -> Tuple[bool, str, str]:
    if no_players_online(response, server_status):
        return False, '', ''

    players = response.players
    online_player = players.online
    max_player = players.max

    online_players = get_players_name(players)

    description = f'''{online_players}\n\n{online_player}/{max_player} player(s) online'''

    return True, 'Online Player(s)', description
