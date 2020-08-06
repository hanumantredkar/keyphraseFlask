from flask import Flask 
from flask import render_template, url_for, request, redirect
# from app import app
# from functions import *


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
  
@app.route('/keyphrases', methods=["POST", "GET"])
def keyphrases():
  user = {'username': 'hanubab'}
  # return '<h1>Hello Mr. '+ user['username'] +'<h1>'
  return render_template('keyphrases.html', title='Home', user=user)
  
# @app.route('/login  ', methods=["POST", "GET"])
# def test():
  # if request.method == "POST":
    # user = request.form["nm"]
    # user = {'username':request.form['nm']}
    # return redirect(url_for('keyphrases', user=user))
  # else:
    # return render_template("test.html")
  # return render_template('test.html', user=user)
  # return render_template('test.html', user={'username':'Rameshwaram'})

@app.route('/login', methods=["POST", "GET"])
def login():
  user={'username':'Ram'}
  # if request.method == 'POST'
    # user={'username':'Kanyakumari'}
  # else
    # user={'username':'Rameshwaram'}
  return render_template('login.html', user=user )  

@app.route('/<usr>')
def user(usr):
  return f"<h1>{usr}</h1>"


@app.route('/main', methods=["POST", "GET"])
def main():
  user={'username':'Ram'}
  return render_template('form.html', user=user)
  

@app.route('/submit', methods=['POST'])
def submit():
  return 'You entered: {}'.format(request.form['inputreviews'])

# @app.route('/engine', methods=['POST'])
# def engine():
  # inputTextDict = {1: 'The product is the best version of itself. I liked its make. I liked its features. I liked its appearence. Overall it is fantabulous.', 2: 'This is going to be the worst product. I like it but it is not as per my expectation. I am not recommending this product. Thankks'}

  # inputLocationDict = {1: 'Mapusa', 2: 'Panjim'}
  
  # dictFinalKeyphrasesLocation = runKeyphraseEngine(inputTextDict, inputLocationDict)


  # print('\nKEYPHRASE : LOCATION')
  # for keyphrase, location in dictFinalKeyphrasesLocation.items():
  # print(keyphrase, '\t', location)