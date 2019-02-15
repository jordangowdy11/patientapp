Feature: Admin viewing the list of Patients

Scenario: Get the Participant list from API
	Given Request for all patients
	Then Have all the patients from the API
	
Scenario: Add Patients using API
	Given a set of patients for API
	|patient_name	|patient_email			|patient_password		|sex	|age	|current_location	|bloodtype	|
	|Jordan			|jj@test.com			|relflf					|Female	|23		|Leeds				|A-			|
	Then increases Patient Count from API

Scenario: Get the Patient List from Browser
	Given Request for patient from browser page
	Then able to fetch the patient count
	
Scenario: Add Patient details using register page
	Given a set of patients for form
	|patient_name			|patient_email				|patient_password		|sex	|age	|current_location	|bloodtype	|
	|Browser Test			|browser@test.com			|relflf					|Female	|23		|York				|A-			|
	Then increases patient count from browser
