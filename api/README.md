# News Desk Text Classifier API

> This API wraps a LinearSVC model to predict news desk label (subject) of a given text. It was trained over 20 thousand NYT Articles from past 18 months.

## Requirements

* `docker` >= 19.03.9
* `docker-compose` >= 1.25.0

## How to run

### 1. Setup Virtual Environment

```bash
docker-compose up --build
```

docker build -t myimage .

docker run -d --name mycontainer -p 8000:8000 myimage

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
