from pathlib import Path
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = (BASE_DIR / "krishiBid.db").as_posix()

class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "dev-secret-key"