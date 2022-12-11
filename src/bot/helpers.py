from os import getenv

from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")


def is_app_mode(mode: str):
    return getenv('APP_ENV') == mode


def get_command_list():
    command_list = {
        'help': 'Show help message',
        'command': 'Show command list',
        'register': 'Register channel to receive server status notifications',
        'unregister': 'Unregister channel from receiving server status notifications',
        'address': 'Get minecraft server address',
        'version': 'Get minecraft version on server',
        'status': 'Get minecraft server status',
        'players': 'Get list of online players',
        # 'start': 'Start the minecraft server',
        # 'stop': 'Stop the minecraft server',
        # 'restart': 'Restart the minecraft server'
    }

    if is_app_mode('development'):
        command_list['clear'] = 'Clear all messages in this channel'

    return command_list
