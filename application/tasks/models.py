from application import db
from application.models import Base

from sqlalchemy.sql import text
from sqlalchemy.orm import relationship

class Trip(Base):

    name = db.Column(db.String(144))

    owner_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    def __init__(self, name):
        self.name = name

class TripParticipant(Base):

    participant_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))

    participant = relationship("User")
    trip = relationship("Trip", backref="participants")

    def __init__(self, participant_id, trip_id):
        self.participant_id = participant_id
        self.trip_id = trip_id

    @staticmethod
    def delete_participant(id):
        stmt = text("DELETE FROM trip_participant WHERE (id = :id)"
            ).params(id=id) 
        db.engine.execute(stmt)

class Task(Base):

    name = db.Column(db.String(144), nullable=False)
    done = db.Column(db.Boolean, nullable=False)

    packer_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)
    trip = relationship("Trip", backref="tasks")

    def __init__(self, name, trip_id):
        self.name = name
        self.done = False
        self.trip_id = trip_id

    @staticmethod
    def booleanToTrue_task(id):
        stmt = text("UPDATE task SET done = True WHERE (id = :id)"
            ).params(id=id)
        db.engine.execute(stmt)

    @staticmethod
    def booleanToFalse_task(id):
        stmt = text("UPDATE task SET done = False WHERE (id = :id)"
            ).params(id=id) 
        db.engine.execute(stmt)

    @staticmethod
    def delete_task(id):
        stmt = text("DELETE FROM task WHERE (id = :id)"
            ).params(id=id) 
        db.engine.execute(stmt)

    @staticmethod
    def modify_task(id, name):
        stmt = text("UPDATE task SET name = (:name) WHERE (id = :id)"
            ).params(name=name, id=id) 
        db.engine.execute(stmt)