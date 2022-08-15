from os import getenv

from dotenv import load_dotenv
from flask import Flask, render_template

from bot import bot

load_dotenv(dotenv_path="./.env")

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(threaded=True, port=8080)
    bot.run(getenv('DC_TOKEN'))
