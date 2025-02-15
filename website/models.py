from . import db
from flask_login import UserMixin


#user table 
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    dateofbirth = db.Column(db.Date, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    # relationship between the RiskAssessment table and the User table
    risk_assessments = db.relationship('RiskAssessment')
#Risk assessment table 

class RiskAssessment(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #Foreign Key
    # assessment_date = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=True)
    smoke_alarms = db.Column(db.Boolean, nullable=True)
    electrical_cords = db.Column(db.Boolean, nullable=True)
    furniture_secured = db.Column(db.Boolean, nullable=True)
    emergency_plan = db.Column(db.Boolean, nullable=True)
    security_measures = db.Column(db.Boolean, nullable=True)

#health tracking table 
class Myhealth(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    step_count = db.Column(db.Integer, nullable=False)
    sleep_count = db.Column(db.Integer, nullable=False)
    calories_burned = db.Column(db.Integer, nullable=False)