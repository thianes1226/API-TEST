from flask import Flask
from flask import Flask, render_template, request 
from data import eleves
    
app = Flask(__name__)


## creation du route principale qui est le point entre de app 
@app.route("/")
def index(): 
    return "<h1> Bienvenue dans API de Flask-SEMI  templates </h1>"
    return render_template("index.html")

@app.route("/eleves")
def list_eleves(): 
    return render_template("list_eleves.html", students=eleves)


@app.route("/all")
def list_all():
    cl = request.args.get("classe")
    print(cl)
    if cl:
        elvs  = [etd for etd in eleves if etd["classe"] == cl]
        return render_template("test.html", students=elvs)
    else: 
        return render_template("test.html", students=eleves)
    
if __name__ == "__main__": 
    app.run(debug=True )