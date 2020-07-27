import json
import requests
from app import app
from flask import render_template, request, redirect

pŕedictions = []
predict_api_url = 'http://backend:8000/predict/'

@app.route("/")
def index():
    return render_template("public/index.html", pŕedictions=reversed(pŕedictions))

@app.route("/predict", methods=["POST"])
def predict():

    if request.method == "POST":

        req = request.form
        data = {
            'item_id': int(len(pŕedictions) + 1),
            'text': str(request.form["text"])
        }

        j_data = json.dumps(data)
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

        r = requests.post(predict_api_url, data=j_data, headers=headers)

        pŕedictions.append(r.json())

        return redirect("/")

    return render_template("public/index.html")

@app.route("/swagger-docs", methods=["GET"])
def swagger_docs():

    return redirect("http://0.0.0.0:8000/docs")

