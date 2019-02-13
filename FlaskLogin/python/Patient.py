
'''
Created on 13 Feb 2019

@author: Jordan61077
'''

if __name__ == '__main__':
    
    pass

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
    email = db.Column('patient_email',db.String(50))
    password = db.Column('patient_password',db.String(20))
    sex = db.Column(db.String(50))
    age = db.Column(db.Integer)
    current_location = db.Column(db.String(50))
    bloodtype = db.Column(db.String(50))
    
    def __init__(self, params):
        self.name = params['name']
        self.email = params['email']
        self.password = params['password']
        self.sex = params['sex']
        self.age = params['age']
        self.current_location = params['current_location']
        self.bloodtype = params['bloodtype']
    
    def __str__(self):
        return "Id:" + str(self.product_id) + " Name: " + self.name + " Sex: " + self.sex + " Age: " + str(self.age) 
        + " Registered Hospital: " + self.current_location + " bloodtype: " + self.bloodtype
    


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
        self.duration = params['duration']
        self.notes = params['notes']
        self.attending_doctor = params['doctor']    

def example_Patient():
    
    db.session.add(Patient({"name":"Jordan Test","email":"jj@test.com","password":"pass","sex":"Male",
                            "age":22,"current_location":"Leeds","bloodtype":"A+"}))
    db.session.commit()
    patients = Patient.query.all()
    for p in patients:
        print("Id: ",p.patient_id,"name: ",p.name,"email: ",p.email,"password: ",p.password,
              "Sex: ",p.sex,"Age: ",p.age,"current_location: ",p.current_location,"bloodtype:",p.bloodtype)
    
    return patients 



def example_Report():
    r = db.session.add(Report({"date":"12/10/2018","reason":"Diarrhea","duration": 4,"notes":"it was bad","doctor":"Dr Tuts"}))
    #p = Patient({"name":"Alex","sex":"M","age":"10","current_location":"Leeds","bloodtype":"O+"})
       
    db.session.commit()
    report = Report.query.all()
    for r in report:
        print("Id",r.report_id, "Date:",r.date,"Duration:",r.duration,
              "Reason:",r.reason_for_admission,"notes:",r.notes,"Doctor:",r.attending_doctor)
    
    return report
    

if __name__ == '__main__':
    db.create_all()
    example_Report()
    example_Patient()
        
    pass
        
