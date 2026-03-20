import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "your-secret-key"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "postgresql://genshin_web_app_user:eDHECRP4cidXh2U5OkM1QJiRLLJyONdE@dpg-d6ucr9ngi27c73e650v0-a.virginia-postgres.render.com/genshin_web_app"
    SQLALCHEMY_TRACK_MODIFICATIONS = False