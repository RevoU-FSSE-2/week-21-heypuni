from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


secret_key = "Auth12#Secret"
db = SQLAlchemy(model_class=Base)
ma = Marshmallow()
bcrypt = Bcrypt()
