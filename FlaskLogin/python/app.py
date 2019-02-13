'''
Created on 8 Feb 2019

@author: Jordan61077
'''

from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')



if __name__ == '__main__':
    app.run(port = 5500)