from application import db
from application.models import Base

from sqlalchemy.sql import text

class Task(Base):

    name = db.Column(db.String(144), nullable=False)
    done = db.Column(db.Boolean, nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def __init__(self, name):
        self.name = name
        self.done = False

#    @staticmethod
#    def boolean_task(id):
#        stmt = text("DELETE FROM task WHERE (id = :id)"
#            ).params(id=id) 
#        db.engine.execute(stmt)
#
#UPDATE
# Customers
#SET
# City = 'Oslo';

    @staticmethod
    def delete_task(id):
        stmt = text("DELETE FROM task WHERE (id = :id)"
            ).params(id=id) 
        db.engine.execute(stmt)

    #@staticmethod
    #def modify_task(id, ???):
        #stmt = text("UPDATE task SET name = ('???') WHERE (id = :id)"
        #    ).params(id=id) 
    #    db.engine.execute(stmt)