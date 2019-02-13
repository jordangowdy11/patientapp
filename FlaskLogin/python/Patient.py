from flask.app import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
import jsonpickle

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/graduate_training'
db = SQLAlchemy(app)

class Patient(db.Model):
    __tablename__ = "alc_patients"
    
    patient_id = db.Column(db.Integer, primary_key = True)
    name = db.Column('patient_name', db.String(50))
    sex = db.Column(db.String(50))
    age = db.Column(db.Integer)
    current_location = db.Column(db.String(50))
    bloodtype = db.Column(db.String(50))
    
    def __init__(self, params):
        self.name = params['name']
        self.sex = params['sex']
        self.age = params['age']
        self.current_location = params['current_location']
        self.bloodtype = params['bloodtype']
    
    def __str__(self):
        return "Id:" + str(self.product_id) + " Name: " + self.name + " Sex: " + self.sex + " Age: " + str(self.age) 
        + " Registered Hospital: " + self.current_location + " bloodtype: " + self.bloodtype
    
    #reports =

class Report(db.Model):
    __tablename__ = "alc_reports"
    
    report_id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.String(50))
    duration = db.Column(db.Integer)
    reason_for_admission = db.Column(db.String(50))
    notes = db.Column(db.String(200))
    attending_doctor = db.Column(db.String(200))
    
    def __init__(self, params):
        self.date = params['date']
        self.reason_for_admission = params['reason']
        self.notes = params['notes']
        self.attending_doctor = params['doctor']    
    