from flask import current_app
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

client = MongoClient(os.environ.get('DATABASE_URI'))

db = client['flutter_app']
