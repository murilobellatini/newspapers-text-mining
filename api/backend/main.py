"""
Script to run API on localhost:8000
"""

import os
import joblib
import requests
import pathlib as pl
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    text: str
    item_id: int
    prediction: Optional[str] = None

@app.post('/predict/')
def predict_label(item: Item):
    """
    Returns prediction for Text Classification based using
    LinearSVC trained model over 20k articles from New York Times
    """
    item.prediction = id2label[clf.predict(vect.transform([item.text]))[0]]
    
    return item

def load_model(classifier:str, vectorizer:str, id_to_tabel_dict:str):
    """
    Loads classifier, vectorizer and label dictionary for predicting data
    """
    root_path = pl.Path(os.getcwd())
    clf = joblib.load(root_path / f'model/{classifier}.sav')
    vect = joblib.load(root_path / f'model/{vectorizer}.sav')
    id2label = joblib.load(root_path / f'model/{id_to_tabel_dict}.sav')

    return clf, vect, id2label

clf, vect, id2label = load_model('LinearSVC', 'TfidfVectorizer', 'IdToLabelDict')
