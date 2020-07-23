"""
Script to run API
"""

import os
import joblib
import pathlib as pl
from flask import Flask, request, redirect, url_for, flash, jsonify

app = Flask(__name__)

@app.route('/api/', methods=['POST'])
def predict_label():
    """
    Returns prediction based on input `{"text": TEXT_TO_BE_PREDICTED}`
    """
    data = request.get_json()
    text = data['text']
    prediction = id2label[clf.predict(vect.transform([text]))[0]]
    
    return jsonify(prediction)

def load_model(classifier:str, vectorizer:str, id_to_tabel_dict:str):
    """
    Loads classifier, vectorizer and label dictionary for predicting data
    """
    root_path = pl.Path(os.getcwd())
    clf = joblib.load(root_path / f'model/{classifier}.sav')
    vect = joblib.load(root_path / f'model/{vectorizer}.sav')
    id2label = joblib.load(root_path / f'model/{id_to_tabel_dict}.sav')

    return clf, vect, id2label

if __name__ == '__main__':
    clf, vect, id2label = load_model('LinearSVC', 'TfidfVectorizer', 'IdToLabelDict')
    app.run(debug=True, host='0.0.0.0')
