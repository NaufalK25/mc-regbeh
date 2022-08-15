from os import getenv

from dotenv import load_dotenv

from app.main import app
from app.bot import bot

load_dotenv(dotenv_path="./.env")

if __name__ == "__main__":
    bot.run(getenv('DC_TOKEN'))
    app.run()
