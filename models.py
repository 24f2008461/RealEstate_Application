from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from datetime import timezone

db = SQLAlchemy()


class User(db.Model,UserMixin):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True) # user id is unique
    username = db.Column(db.String(80), unique=True, nullable=False) # username should be unique
    fullname = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(40), nullable=False,default='client')
    dob = db.Column(db.Date, nullable=False)
    phone = db.Column(db.String(20), unique=True,nullable=False)
    email = db.Column(db.String(100) ,unique=True, nullable=False)
    status = db.Column(db.String(20),nullable=False,default='pending')
    created_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # relationships
    plot_seller = db.relationship("RealEstate", backref='seller' , lazy=True)
    plot_visitor = db.relationship('Visiting' , backref='visitor', lazy=True)


    def __repr__(self):
        return f"<USER {self.username}>"

class RealEstate(db.Model):

    __tablename__ = 'realestate'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    state = db.Column(db.String(30), nullable=False)
    district = db.Column(db.String(40), nullable=False)
    area = db.Column(db.String(100), nullable=False)
    landmark = db.Column(db.String(200), nullable=False)
    bhk = db.Column(db.Integer, nullable=True) # Applicable for apartments/villas
    area_sqft = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Numeric(15,2),nullable=False)
    property_type = db.Column(db.String(50), nullable=False, default='plot')
    plot_no = db.Column(db.String(100), nullable=False)
    registered_owner_id = db.Column(db.Integer, db.ForeignKey("user.id"),nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    scheduled_visits = db.relationship("Visiting", backref='visit', lazy=True)
    images = db.relationship("PropertyImage", backref='property', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<REALESTATE {self.id}>"
    
class PropertyImage(db.Model):
    __tablename__ = 'property_image'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    property_id = db.Column(db.Integer, db.ForeignKey('realestate.id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)
    uploaded_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<PROPERTY_IMAGE {self.id}>"



class Visiting(db.Model):

    __tablename__ = 'visiting'

    visiting_id  =  db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"),nullable=False)
    plot_id = db.Column(db.Integer, db.ForeignKey("realestate.id"),nullable=False)
    visiting_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String, nullable=False,default='pending')
    broker_notes = db.Column(db.Text, nullable=True)
    created_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<VISITING {self.visiting_id}>"