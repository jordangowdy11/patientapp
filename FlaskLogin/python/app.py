'''
Created on 8 Feb 2019

@author: Jordan61077
'''

from flask import Flask, render_template
import jsonpickle
from python.Patient import Patient

#from data import Areas



app = Flask(__name__)

#Areas = Areas()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')


    
    
    


if __name__ == '__main__':
    app.run(port = 5500)