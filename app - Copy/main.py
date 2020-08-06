from flask import Flask 
from flask import render_template, url_for, request, redirect

# from functions import *


app = Flask(__name__) 


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
  return render_template('main.html', user=user)
  
# @app.route('/extractedKeyphrases', methods=['POST'])
# def extractedKeyphrases():
  # dictExtractedKeyAndLocations = {}
  # dictExtractedKeyAndLocations = runMyCodeForExtractingKeyphrases()
  # return str(dictExtractedKeyAndLocations)  
  # return 'You entered: {}'.format(request.form['inputreviews']) 


# @app.route('/submit', methods=['POST'])
# def submit():
  # result = request.form['inputreviews']
  # return 'Extracted Keyphrases: {}'.format(result)

@app.route('/submit', methods=['POST'])
def submit():
  result = request.form['inputreviews']
  # count = 1
  # inputTextDict = {}
  # NoOfInputs = 2
  # inputStr = ''
  # output = ''
  # for count in range(1, NoOfInputs):
    # inputStr += count+':'+result
  # dictInputStr = {}
  # dictInputStr = eval(dictInputStr)
  # dictFinalKeyphrasesLocation = inputStr
  dictFinalKeyphrasesLocation = extractedKeyphrases()
  return 'Extracted Keyphrases: {}'.format(dictFinalKeyphrasesLocation)
  
 
#rendering the HTML page which has the button
# @app.route('/json')
# def json():
    # return render_template('json.html')

def extractedKeyphrases():
    dictExtractedKeyAndLocations = {}
    dictExtractedKeyAndLocations = runMyCodeForExtractingKeyphrases()
    return str(dictExtractedKeyAndLocations)    
    
def runMyCodeForExtractingKeyphrases():
  # This is a test function 
  inputTextDict = {1: 'The product is the best version of itself. I liked its make. I liked its features. I liked its appearence. Overall it is fantabulous.', 2: 'This is going to be the worst product. I like it but it is not as per my expectation. I am not recommending this product. Thankks'}

  inputLocationDict = {1: 'Mapusa', 2: 'Panjim'}
    
  # dictFinalKeyphrasesLocation = runKeyphraseEngine(inputTextDict, inputLocationDict)
  
  dictFinalKeyphrasesLocation = inputTextDict

  # print('\nKEYPHRASE : LOCATION')
  # for keyphrase, location in dictFinalKeyphrasesLocation.items():
    # print(keyphrase, '\t', location)
  
  return dictFinalKeyphrasesLocation
  
  