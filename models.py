from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime


db = SQLAlchemy()


class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True) # user id is unique
    username = db.Column(db.String(80), unique=True, nullable=False) # username should be unique
    fullname = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(40), nullable=False,default='user')
    date_of_birth = db.Column(db.DateTime, nullable=False)
    phone = db.Column(db.String(20), unique=True,nullable=False)
    email = db.Column(db.String(100) ,unique=True, nullable=False)
    status = db.Column(db.String(20),nullable=False,default='pending')
    created_date = db.Column(db.DateTime, default=datetime.utcnow)


    plots_listed = db.relationship("RealEstate", backref='seller' , lazy=True)
    plot_visits = db.relationship('Visiting' , backreg='visitor', lazy=True)


    def __repr__(self):
        return f"<USER {self.username}>"

class RealEstate(db.Model):

    __tablename__ = 'realestate'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    state = db.Column(db.String(30), nullable=False)
    district = db.Column(db.String(40), nullable=False)
    area = db.Column(db.String(100), nullable=False)
    landmark = db.Column(db.String(200), nullable=False)
    cost = db.Column(db.Integer,nullable=False)
    plot_no = db.Column(db.String(100), nullable=False)
    registered_owner_id = db.Column(db.Integer, db.ForeignKey("user.id"),nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)


    scheduled_visits = db.relationship("Visiting", backref='visit', lazy=True)

    def __repr__(self):
        return f"<REALESTATE {self.id}>"


class Visiting(db.Model):

    __tablename__ = 'visiting'

    visiting_id  =  db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"),nullable=False)
    plot_id = db.Column(db.Integer, db.ForeignKey("realestate.id"),nullable=False)
    visiting_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String, nullable=False,default='pending')
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<VISITING {self.visiting_id}>"