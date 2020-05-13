#-*- coding:utf-8 -*-
from flask import Flask, render_template

application = Flask(__name__)
application.env = 'development'
application.debug = True


@application.route('/')
@application.route('/<user>')
def index(user='상호'):
    return render_template('entry.html', name=user)
    # url test1 request path /두루
    # url test2 request path /


@application.route('/gpio')
def gpio():
    return render_template('main2.html')

@application.route("/<changePin>/<action>")
def action (changePin, action):
    changePin = int(changePin)
    deviceName = pins[changePin]['name']
    templateData = {
        'message' : 'message',
        'pin' : 'pins'
    }
    return render_template('main2.html', **templateData)


#admin PAGE
#@app.route('/AD')

# Run the application
if __name__ == "__main__":
    application.run(host="0.0.0.0")
