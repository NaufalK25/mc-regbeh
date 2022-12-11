from os import getenv

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv(dotenv_path="./.env")

client = MongoClient(getenv('MONGO_URI'))

database = client.get_database(getenv('MONGO_DB'))
