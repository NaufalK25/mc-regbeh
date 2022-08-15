from os import getenv

from dotenv import load_dotenv
from flask import Flask, render_template

from bot.bot import bot

load_dotenv(dotenv_path="./.env")

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


app.run(threaded=True, port=5000)
