# Digital Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Run api.py file in `./src` directory using below command.

```bash
python api.py
```

If you are using an IDE like pycharm, open `api.py` file in `./src` directory and hit run button.

## Testing

In this project we have used Postman collections to test all the endpoints for expected behavior including permission checks.

To execute these tests follow the steps below:

- Install PostmanREST client
- Download the postman collection 'endpoints_postman_collection.json' from this directory.
- Open Postman application and follow the navigation. Menu -> File -> Import -> select the json file you just downloaded -> Click OK.
- Hit Runner button and select the collection to run.

>Note: 
>1. Run your flask server before running Postman collection.
>2. You may need to update tokens in Postman collection before running the tests as the tokens specified might have already expired.

## API Reference

### Getting Started

- Base URL: Currently this application is hosted locally. The backend is hosted at http://127.0.0.1:5000/
- Authentication and Authorization: This application is configured to work with [auth0](https://auth0.com/) which uses the OpenID Connect (OIDC) Protocol and OAuth 2.0 Authorization Framework to authenticate users and get their authorization to access protected resources.

### Error Handling

Errors are returned as JSON in the following format:

```bash
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

The API will return these error types when requests fail.

- 400: bad request
- 401: unauthorized
- 405:: method not implemented
- 422: unprocessible entity
- 500: internal server error

### Endpoints

GET /drinks

- Fetches all the drink details in short data representation (only color and parts are included in response, but not namee field).
- Sample response:
```bash
{
  "drinks": [
    {
      "id": 1, 
      "recipe": [
        {
          "color": "Blue", 
          "parts": 2
        }, 
        {
          "color": "Green", 
          "parts": 1
        }, 
        {
          "color": "orange", 
          "parts": 3
        }
      ], 
      "title": "Mocca"
    }
  ],
  "success": true
}
```

GET /drinks-detail

- Fetches all the drink details in long data representation (full recipe details are included in response) if the user has 'get:drinks-detail' permission.
- Sample response:
```bash
{
  "drinks": [
    {
      "id": 1, 
      "recipe": [
        {
          "color": "Blue", 
          "name": "BlueBerry", 
          "parts": 2
        }, 
        {
          "color": "Green", 
          "name": "GreenBerry", 
          "parts": 1
        }, 
        {
          "color": "orange", 
          "name": "Orange", 
          "parts": 3
        }
      ], 
      "title": "Mocca"
    }
  ], 
  "success": true
}
```

POST /drinks

- Creates a new drink if user has 'post:drinks' permission
- Sample request:
```bash
{
	"id": -1,
	"title": "Cappucino",
	"recipe": [{
		"name": "blueberry",
		"color": "Blue",
		"parts": 2
	}, {
		"name": "cranberry",
		"color": "red",
		"parts": 2
	}]
}
```
- Sample response:
```bash
{
  "drinks": [
    {
      "id": 2, 
      "recipe": [
        {
          "color": "Blue", 
          "name": "blueberry", 
          "parts": 2
        }, 
        {
          "color": "red", 
          "name": "cranberry", 
          "parts": 2
        }
      ], 
      "title": "Cappucino"
    }
  ], 
  "success": true
}
```

PATCH /drinks/<drink_id>

- updates drink details if user has 'patch:drinks' permission.
- Request Arguments: drink_id: int
- Sample request:
```bash
{
	"id": 1,
	"recipe": [{
		"color": "Blue",
		"name": "BlueBerry",
		"parts": 2
	}, {
		"color": "Green",
		"name": "GreenBerry",
		"parts": 1
	}, {
		"color": "orange",
		"name": "Fresh Orange",
		"parts": 2
	}],
	"title": "Mocca"
}
```

- Sample response:
```bash
{
  "drinks": [
    {
      "id": 1, 
      "recipe": [
        {
          "color": "Blue", 
          "name": "BlueBerry", 
          "parts": 2
        }, 
        {
          "color": "Green", 
          "name": "GreenBerry", 
          "parts": 1
        }, 
        {
          "color": "orange", 
          "name": "Fresh Orange", 
          "parts": 2
        }
      ], 
      "title": "Mocca"
    }
  ], 
  "success": true
}

```

DELETE /drinks/<drink_id>

- deletes a drink with specified id from the database if the user has 'delete:drinks' permission.
- Request Arguments: drink_id: int
- Sample response:
```bash
{
  "deleted": 3, 
  "success": true
}
```
