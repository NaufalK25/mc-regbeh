from os import getenv
from threading import Thread

from dotenv import load_dotenv
from flask import Flask, render_template

from bot import bot

load_dotenv(dotenv_path="./.env")

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


def run():
    app.run(threaded=True, port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()


bot.run(getenv('DC_TOKEN'))
