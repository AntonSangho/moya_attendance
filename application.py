#-*- coding:utf-8 -*-
from flask import Flask, render_template

application = Flask(__name__)
application.env = 'development'
application.debug = True


@app.route('/')
@app.route('/<user>')
def index(user='상호'):
    return render_template('entry.html', name=user)
    # url test1 request path /두루
    # url test2 request path /


#admin PAGE
#@app.route('/AD')

# Run the application
if __name__ == "__main__":
    application.run(host="0.0.0.0")
