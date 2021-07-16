import os
from dotenv import load_dotenv

load_dotenv()

db=os.getenv('DATABASE_URL')
if db.startswith('postgres://'):
    db=db.replace("postgres://", "postgresql://", 1)
class Config:
    SQLALCHEMY_DATABASE_URI=db
    SECRET_KEY=os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    

class TestConfig:
    TESTING=True
    SQLALCHEMY_DATABASE_URI='sqlite:///test.db'
    SECRET_KEY=os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    