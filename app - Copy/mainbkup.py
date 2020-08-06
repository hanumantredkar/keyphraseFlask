from flask import Flask 
from flask import render_template, url_for, request, redirect
# from app import app
app = Flask(__name__) 

# from app import routes

@app.route('/')
@app.route('/index', methods=["POST", "GET"])
def home_view():
  # if request.method == "POST":
    # user = request.form["inputreviews"]
    # return redirect(url_for('keyphrases', usr=user))
  # else:
    # return render_template("index.html")
  return render_template('index.html', title='Home', user='Hanumant Redkar')
  
# @app.route('/')
@app.route('/keyphrases', methods=["POST", "GET"])
def keyphrases():
  user = {'username': 'hanubab'}
  # return '<h1>Hello Mr. '+ user['username'] +'<h1>'
  return render_template('keyphrases.html', title='Home', user=user)
  
@app.route('/login2  ', methods=["POST", "GET"])
def test():
  if request.method == "POST":
    # user = request.form["nm"]
    user = {'username':request.form['nm']}
    # return redirect(url_for('keyphrases', user=user))
  # else:
    # return render_template("test.html")
  return render_template('test.html', user=user)
  # return render_template('test.html', user={'username':'Rameshwaram'})

# @app.route('/login', methods=["POST", "GET"])
# def login():
  # return render_template('login.html', user={'username':'Rameshwaram'})  
# @app.route('/<usr>')
# def user(usr):
  # return f"<h1>{usr}</h1>"

# from flask import Flask, request, render_template

# app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    return 'You entered: {}'.format(request.form['inputreviews'])