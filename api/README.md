# News Desk Text Classifier API

> This API wraps a LinearSVC model to predict news desk label (subject) of a given text. It was trained over 20 thousand NYT Articles from past 18 months.

## Requirements

* `docker >= 19.03.9`
* `docker-compose >= 1.25.0`

## How to run

### 1. Build and run docker

```bash
docker-compose up --build
```

### 2. Test API

> Expected outcome is `<Response [200]> "Politics"`

```bash
python test.py
```

## API Routes

`GET /docs`

> Returns current documentation of API methods

`POST /predict`

> Returns prediction of label for given text in format below

### Example

#### Request Header

```json
{
    "content-type": "application/json",
    "Accept-Charset": "UTF-8"
}
```

#### Request Body

```json
{
    "item_id": 1,
    "text": "Trump Steps Up His Assault on Biden With Scattershot Attacks, Many False"
}
```

#### Response

```json
{
    "item_id": 1,
    "text": "Trump Steps Up His Assault on Biden With Scattershot Attacks, Many False",
    "prediction": "Politics"
}
```
