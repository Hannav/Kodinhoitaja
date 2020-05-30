from application import db
from application.models import Base

from sqlalchemy.sql import text

#https://flask-login.readthedocs.io/en/latest/#your-user-class
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

#Näytä keillä on pakattavaa:
#    @staticmethod
#    def find_users_with_no_tasks(done=False):
#        stmt = text("SELECT Account.id, Account.name FROM Account"
#                     " LEFT JOIN Task ON Task.account_id = Account.id"
#                     " WHERE (Task.done IS null OR Task.done = :done)"
#                     " GROUP BY Account.id"
#                     " HAVING COUNT(Task.id) = 0").params(done=done)
#        res = db.engine.execute(stmt)
#
#        response = []
#        for row in res:
#            response.append({"id":row[0], "name":row[1]})
#
#        return response
    
    @staticmethod
    def create_user(username, password):
        stmt = text("INSERT INTO account (name, username, password) VALUES (:username, :username, :password)"
            ).params(username=username, password=password)
        db.engine.execute(stmt)