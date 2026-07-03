from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))

db = client["Yazhi"]

login_collection = db["login"]
otp_collection = db["otp"]
pro_collection = db["pro"]
attendance_collection = db["attendance"]