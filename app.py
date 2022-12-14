from flask import Flask, render_template, url_for, request
import requests

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/consent")
def consent():
    return render_template("queres.html")

@app.route("/doineedit")
def doineedit():
    a = request.args.get("lat")[:7]
    b = request.args.get("long")[:7]
    r = requests.get(url=f"https://api.open-meteo.com/v1/forecast?latitude={a}&longitude={b}&daily=precipitation_sum&timezone=auto").json()
    
    y, x = r["daily"]["precipitation_sum"][:2]

    res = "No, you won't"
    c = "cat_ok"
    if x > 0.5:
        res = "Yes, you will"
        c = "cat"

    lat_long_formatted = a + "," + b

    return render_template("result.html", res=res, prec=(x,y), llf=lat_long_formatted, c=c)

@app.route("/denied")
def denied():
    return render_template("fail.html")

if __name__ == "__main__":
    app.run(debug=True)