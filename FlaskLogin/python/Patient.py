
'''
Created on 13 Feb 2019

@author: Jordan61077
'''

from flask.app import Flask
from flask import Flask, render_template, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
import jsonpickle
from werkzeug.utils import redirect

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/graduate_training'
db = SQLAlchemy(app)

#Routes to html pages
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/login')
def login_page():
    return render_template('login.html')




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
    
    reports = db.relationship('Report',
                              backref = db.backref('patient', lazy=True))
    
    def __init__(self, params):
        self.name = params['patient_name']
        self.email = params['patient_email']
        self.password = params['patient_password']
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
    patient_id = db.Column(db.Integer,
                        db.ForeignKey('alc_patients.patient_id'), nullable = False)
    #One Patient => report
    def __init__(self, params):
        self.date = params['date']
        self.reason_for_admission = params['reason']
        self.duration = params['duration']
        self.notes = params['notes']
        self.attending_doctor = params['doctor'] 
 
           
@app.route('/api/reports/list')
def fetch_all_reports():
    for r in Report.query.all():
        print(r.patient.name)
    return jsonpickle.encode(Report.query.all())
    pass


@app.route('/api/patients/list')
def fetch_all_patients():
    return jsonpickle.encode(Patient.query.all())

@app.route('/web/patients')
def display_patients():
    return render_template("/patients.html", result = Patient.query.all(),content_type="application/json")

@app.route('/patients/<int:patient_id>')
def find_patient_by_id(patient_id):
    p = Patient.query.filter_by(patient_id = patient_id).first()
    return jsonpickle.encode(p)

@app.route('/reports/patient/<int:patient_id>')
def find_reports_by_patient(patient_id):
    r = Report.query.filter_by(patient_id = patient_id).all()
    return jsonpickle.encode(r)

@app.route('/web/reports')
def reports():
    return render_template("/reports.html", result = Report.query.all(),content_type="application/json")
        
@app.route('/web/patient_details/<int:patient_id>')
def display_patient_details(patient_id):
    return render_template("/patient_details.html", result = {"pid": patient_id, "reports": jsonpickle.decode(find_reports_by_patient(patient_id))}, 
                           content_type = "application/json")
    
@app.route('/api/insert-patient', methods = ['POST'])
def insert_Patient():
    db.session.add(
        Patient({
            "patient_name": request.form.get('patient_name'),
            "patient_email": request.form.get('patient_email'),
            "patient_password": request.form.get('patient_password'),
            "sex": request.form.get('sex'),
            "age": request.form.get('age'),
            "current_location": request.form.get("current_location"),
            "bloodtype": request.form.get("bloodtype"),
            
            }))
    db.session.commit()
    patients = Patient.query.all()
    for p in patients:
        print("Id: ",p.patient_id,"name: ",p.name,"email: ",p.email,"password: ",p.password,
              "Sex: ",p.sex,"Age: ",p.age,"current_location: ",p.current_location,"bloodtype:",p.bloodtype)
    return jsonpickle.encode(patients)

@app.route("/api/insert-report", methods = ['POST'])
def insert_Report():

    r =  Report({
            "date": request.form.get('date'),
            "reason": request.form.get('reason'),
            "duration": request.form.get('duration'),
            "notes": request.form.get('notes'),
            "doctor": request.form.get('doctor'),
            "patient_id": request.form.get('patient_id')
            })
    p = Patient.query.filter_by(patient_id = request.form.get('patient_id')).first()
    p.reports.append(r)
    db.session.add(r)
    
    db.session.commit()
    report = Report.query.all()
    for r in report:
        print("Id",r.report_id, "Date:",r.date,"Duration:",r.duration,
              "Reason:",r.reason_for_admission,"notes:",r.notes,"Doctor:", r.attending_doctor,
              "Patient Id:", r.patient_id)
    return jsonpickle.encode(report)


@app.route("/api/patient/delete/<int:patient_id>",methods=['DELETE'])
def remove_patient(patient_id):
    p = Patient.query.filter_by(patient_id = patient_id).first()
    db.session.delete(p)
    db.session.commit()
    return jsonpickle.encode(p)
   

@app.route("/api/report/delete/<int:report_id>",methods=['DELETE'])
def remove_report(report_id):
    r = Report.query.filter_by(report_id=report_id).first()
    db.session.delete(r)
    db.session.commit()

    return jsonpickle.encode (r)



@app.route("/web/insert-report", methods = ['POST'])
def web_insert_report():

    r =  Report({
            "date": request.form.get('date'),
            "reason": request.form.get('reason'),
            "duration": request.form.get('duration'),
            "notes": request.form.get('notes'),
            "doctor": request.form.get('doctor'),
            "patient_id": request.form.get('patient_id')
            })
    p = Patient.query.filter_by(patient_id = request.form.get('patient_id')).first()
    p.reports.append(r)
    db.session.add(r)
    db.session.commit()
    report = Report.query.all()
    for r in report:
        print("Id",r.report_id, "Date:",r.date,"Duration:",r.duration,
              "Reason:",r.reason_for_admission,"notes:",r.notes,"Doctor:", r.attending_doctor)
    return redirect("web/patient_details/" + str(request.form.get('patient_id')))

@app.route('/web/register', methods = ['POST'])
def web_register_patient():
    db.session.add(
        Patient({
            "patient_name": request.form.get('patient_name'),
            "patient_email": request.form.get('patient_email'),
            "patient_password": request.form.get('patient_password'),
            "sex": request.form.get('sex'),
            "age": request.form.get('age'),
            "current_location": request.form.get("current_location"),
            "bloodtype": request.form.get("bloodtype")
            }))
    db.session.commit()
    patients = Patient.query.all()
    for p in patients:
        print("Id: ",p.patient_id,"name: ",p.name,"email: ",p.email,"password: ",p.password,
              "Sex: ",p.sex,"Age: ",p.age,"current_location: ",p.current_location,"bloodtype:",p.bloodtype)
    return redirect("/web/patients")

@app.route("/web/patient/delete/<int:patient_id>",methods=['GET'])
def remove_web_patient(patient_id):
    p = Patient.query.filter_by(patient_id = patient_id).first()
    db.session.delete(p)
    db.session.commit()
    return redirect("/web/patients")

@app.route("/web/report/delete/<int:report_id>",methods=['GET'])
def remove_web_report(report_id):
    r = Report.query.filter_by(report_id=report_id).first()
    db.session.delete(r)
    db.session.commit()

    return redirect("/web/reports")


if __name__ == '__main__':

    db.create_all()
    #example_Report()
    #example_Patient()    
    #db.create_all()
    app.run(port=5500)

    pass
        
