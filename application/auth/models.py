from application import db
from application.models import Base

from sqlalchemy.sql import text

class User(Base):

    __tablename__ = "account"

#create table-lauseet:
    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)

    tasks = db.relationship("Task", backref='account', lazy=True)
  
    def __init__(self, name):
        self.name = name

    def get_id(self):
        return self.id
  
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    @staticmethod
    def create_user(username, password):
        stmt = text("INSERT INTO account (name, username, password) VALUES (:username, :username, :password)"
            ).params(username=username, password=password)
        db.engine.execute(stmt)