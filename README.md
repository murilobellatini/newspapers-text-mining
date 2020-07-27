# Data Science Project - Newspapers Text Mining 

> Development repo of end-to-end Data Science project for extracting insights from Newspaper articles via Text Mining toolkit

#### Results achieved so far

1. LinearSVC Text Classifier with 82% accuracy for predicting 6 labels (from Politics to Sports) available via containerized API
2. XGBoost Classifier with 92% accuracy for predicting unsupervised generated labels of also 6 different subjects

## Scope

The main goal of this project is to build a production ready Text Classifier wrapped inside an API in order to showcase how I personally approach Data Science problems specifically when it comes to Text Mining.

Therefore I usually follow the steps below, which are explained as follows:

1. ``Data Extraction``: extract newspaper articles using avaible API's ([notebooks](notebooks/extracting))
2. ``Data Processing``: clean the data before diving in ([notebooks](notebooks/processing))
3. ``Exploratory Data Analysis (EDA)``: draw insights via Sentiment Analysis ([notebooks](notebooks/eda))
4. ``Modeling``: build a supervised Text Classifier and clusterize articles using GloVe Word2Vec ([notebooks](notebooks/modeling))
5. ``Productization``: deploy Text Classifier via API end-point ([api](api))

## Applied Technologies

All technologies involved in this project are described below more or less in the order of the notebooks.

* `Feature Extraction`: Tfidf Vectorizer and RegEx
* `Supervised Learning`: LinearSVC, Logistic Regression, Multinomial Naive Bayes, Random Forest and XGBoost Classifiers
* `Clustering`: DBSCAN and K-Means
* `Transferred Learning`: GloVe Word2Vec
* `Dimensionality Reduction`: t-SNE
* `Statistical Testing`: Chi Squared for words correlations to labels
* `Model Selection`: Train Test Split and K-Fold Cross Validation
* `API`: Data Extraction from NYT, Sentiment Analysis with TextBlob, Productization / Deployment with FastAPI

> **Main libraries and frameworks**: scikit-learn, xgboost, textblob, fastapi, pandas, numpy, seaborn, matplotlib, docker, docker-compose

## How to run

### Requirements

* `python >= 3.6`
* `conda`: [Miniconda Python 3](https://docs.conda.io/en/latest/miniconda.html).

### Step-by-step guide

* Create `conda` environment based on `yml` file.

```bash
conda env create -f environment.yml
```

* Activate `conda` environment.

```bash
conda activate ds-env
```

* Run notebooks as you wish

## Folder organization

    ├── README.md                   <- The top-level README for scientists and engineers.
    │
    ├── api                         <- API folder with containerized Text Classifier
    │
    ├── data                        <- Data folder (versioned in the cloud, not with git)
    │   ├── external                <- Data from third party sources.
    │   ├── interim                 <- Intermediate data that has been transformed.
    │   ├── processed               <- The final, canonical data sets for modeling.
    │   └── raw                     <- The original, immutable data dump.
    │
    ├── models                      <- Trained and serialized models (versioned in the cloud, not with git)
    │
    ├── notebooks                   <- Notebooks folder 
    │
    ├── credentials                 <- Required credentials stored locally (ignored on repo for security issues)
    │
    ├── reports                     <- Code-free, stakeholders-ready reports such as markdown files
    │   ├── figures                 <- Graphics and figures to be used in reporting
    │   └── data                    <- Output data generated by models or analyses
    │
    ├── environment.yml             <- The conda env file for reproducing the environment
    │
    ├── setup.py                    <- makes 'src' installable so it can be imported
    │
    └── src                         <- Reusable Python code
        ├── __init__.py             <- Makes src a Python module
        └── ...                     <- Further modules as work in progress
