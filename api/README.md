# News Desk Text Classifier API

> This API wraps a LinearSVC model to predict news desk label (subject) of a given text. It was trained over 20 thousand NYT Articles from past 18 months.

## Requirements

* `Python 3.7.6`
* `pipenv`

## How to run

### 1. Setup Virtual Environment

```bash
pipenv shell
pip install -r requirements.txt
```

### 2. Run API on port 8000 of `localhost`

```bash
pipenv shell
uvicorn app:app --reload
```

### 3. Test API

> Expected outcome is `<Response [200]> "Politics"`

```bash
pipenv shell
python test.py
```

## API Routes

`POST /api`

### Request example

#### Header

```json
{"content-type": "application/json", "Accept-Charset": "UTF-8"}
```

#### Body

##### Input

```json
{
    "item_id": 1,
    "text": "Trump Steps Up His Assault on Biden With Scattershot Attacks, Many False"
}
```

##### Output

```json
{
    "item_id": 1,
    "text": "Trump Steps Up His Assault on Biden With Scattershot Attacks, Many False",
    "prediction": "Politics"
}
```
