import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL') or 'sqlite:///app.db'
    SECRET_KEY=os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    

class TestConfig:
    TESTING=True
    SQLALCHEMY_DATABASE_URI='sqlite:///test.db'
    SECRET_KEY=os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    