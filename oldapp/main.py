from flask import Flask 

app = Flask(__name__) 

@app.route("/") 
def home_view():
    #str = "<h2> Testing if string works fine </h2> </br> <h1> Hanu's Flask </h1>"
    str = "Hello Mr. {name}!"
    return str

#@app.route("/")
#def user(name):
#    return f"Hello Mr. {name}!"
#    return render_template("index.html")
#    return "<h1>Understanding Flask Framework with Heroku</h1>"
    
#if __name__ == "__main__": 
#    app.run()