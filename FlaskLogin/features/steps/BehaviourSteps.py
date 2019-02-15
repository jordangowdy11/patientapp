'''
Created on 14 Feb 2019

@author: Jordan61077
'''
import behave
from nose.tools.trivial import ok_
from pip._vendor import requests
from selenium import webdriver

@given('Request for all patients')
def fetch_patients_from_api(context):
    context.patients = requests.get("http://localhost:5500/api/patients/list").json()

@then('Have all the patients from the API')
def check_all_patients_are_present(context):
    ok_(len(context.patients)>0,"Patients not found")
    
@given('a set of patients for API')
def post_patients_to_api(context):
    context.currentCount = len(requests.get(
        "http://localhost:5500/api/patients/list").json())
    for row in context.table:
        new_patient = requests.post("http://localhost:5500/api/insert-patient",
                                   data={"patient_name":row["patient_name"],"patient_email":row["patient_email"],
                                         "patient_password":row["patient_password"],"sex":row["sex"],
                                         "age":row["age"],"current_location":row["current_location"],"bloodtype":row["bloodtype"]}).json()
        print(new_patient)
        
@then('increases Patient Count from API')
def check_count_increase(context):
    ok_(context.currentCount<len(requests.get(
        "http://localhost:5500/api/patients/list").json()),"Patient Registration Failed")

@given('Request for patient from browser page')
def request_patients_from_browser(context):
    context.driver = webdriver.Chrome()
    context.driver.get("http://localhost:5500/web/patients")
    context.countText = context.driver.find_element_by_id("count").text
    print(context.countText)
    
@then('able to fetch the patient count')
def check_patient_count(context):
    context.driver.save_screenshot("snaps/Patient.png")
    ok_(len(context.countText)>0,"Patient not found")
    

        
                            
                            
                            
                            
                            