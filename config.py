import os
from dotenv import load_dotenv

load_dotenv()  # .envファイルを読み込む

class Config:
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        