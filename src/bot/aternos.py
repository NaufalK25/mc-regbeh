from os import getenv

from dotenv import load_dotenv
from python_aternos import Client

load_dotenv(dotenv_path="./.env")


class Aternos:
    def __init__(self):
        self.username = getenv("ATERNOS_USERNAME")
        self.password = getenv("ATERNOS_PASSWORD")
        self.client = self.login()
        self.servers = self.get_server_list()

    def login(self):
        return Client.from_credentials(self.username, self.password)

    def get_server_list(self):
        return self.client.list_servers()

    def start(self):
        for server in self.servers:
            if server.address == getenv('MC_SERVER'):
                server.start()

    def stop(self):
        for server in self.servers:
            if server.address == getenv('MC_SERVER'):
                server.stop()

    def restart(self):
        for server in self.servers:
            if server.address == getenv('MC_SERVER'):
                server.restart()
