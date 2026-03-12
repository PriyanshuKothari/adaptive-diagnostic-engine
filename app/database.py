import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME: str = os.getenv("DB_NAME", "adaptive_engine")

client: MongoClient = MongoClient(MONGODB_URI)
db = client[DB_NAME]

questions_col = db["questions"]
sessions_col = db["user_sessions"]
