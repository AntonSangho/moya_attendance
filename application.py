#-*- coding:utf-8 -*-
from flask import Flask, render_template

app = Flask(__name__)
app.env = 'development'
app.debug = True

#@app.route('/<user>')
@app.route('/')
def index():
    return render_template('entry.html', name="두루")


#admin PAGE
#@app.route('/AD')

##
app.run(host='0.0.0.0', port=5000)
