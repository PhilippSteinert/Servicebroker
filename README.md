# Servicebroker

## Motivation
The servicebroker manages *servicerequests*. The current application allows creating, retrieving, updating and deleting *servicerequests*. The final version will be able to handle various *servicerequests* (e.g. transportation, surveillance or inspection). The current application is build around a single application: To handle organ transportation from donor clinic to transplant center.
Hosted on heroku. `https://git.heroku.com/servicebroker.git`

## Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication & authorization: All endpoints require JWT bearer tokens.

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Envirionment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the [PostgreSQL](https://www.postgresql.org/) database. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Tool Structure

```
├── flaskr/
│   ├── __init__.py
├── auth/
│   ├── __init__.py
│   ├── auth.py
├── models.py
├── test_flaskr.py
├── manage.py
├── requirements.txt
├── servicebroker.psql
```

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql servicebroker < servicebroker.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "Bad request."
}
```
The API will return various error types when requests fail:
- 400: Bad request
- 401: Unauthenticated
- 403: Permission not found
- 404: Resource not found
- 422: Unprocessable

### Endpoints 
Endpoints cover 

#### `GET localhost:5000/servicerequests`
- Retrieves servicerequests
- Returns success value, total servicerequests and list of servicerequests
- Results are paginated (every 5 servicerequests)

Header:
| Key             | Value                 | Description                     | Required / Optional         |
|:----------------|:----------------------|:--------------------------------|:----------------------------|
| Authorization   | Bearer &lt;token&gt;  | Requires JWT bearer token       | Required                    |

Response:
``` 
{
  "servicerequests": [
    {
      "collection_datetime": "2020-05-28, 11:30",
      "delivery_datetime": "2020-05-28, 12:30",
      "destination_airport": "Klinikum Grosshadern",
      "id": 1,
      "latest_delivery_datetime": "2020-05-28, 13:30",
      "origin_airport": "Universitaetsklinik Innsbruck",
      "payload": "Kidney",
      "payload_weight": 5,
      "priority": true,
      "service_type": "Organ transport",
      "status": "Requested",
      "user_id": 2
    },
    {
      "collection_datetime": "2020-05-28, 11:30",
      "delivery_datetime": "2020-05-28, 12:30",
      "destination_airport": "Klinikum Grosshadern",
      "id": 2,
      "latest_delivery_datetime": "2020-05-28, 13:30",
      "origin_airport": "Universitaetsklinik Innsbruck",
      "payload": "Kidney",
      "payload_weight": 5,
      "priority": true,
      "service_type": "Organ transport",
      "status": "Requested",
      "user_id": 2
    }
  ],
  "success": true,
  "total_servicerequests": 2
}
```

#### `GET localhost:5000/hospitals`
- Retrieves hospitals
- Returns success value, total hospitals and list of hospital names

Header:
| Key             | Value                 | Description                     | Required / Optional         |
|:----------------|:----------------------|:--------------------------------|:----------------------------|
| Authorization   | Bearer &lt;token&gt;  | Requires JWT bearer token       | Required                    |

Response:
``` 
{
  "hospitals": [
    {
      "id": 1,
      "name": "Klinikum Muenchen Grosshadern"
    },
    {
      "id": 2,
      "name": "Universitaetsklinik Innsbruck"
    }
  ],
  "success": true,
  "total_hospitals": 2
}
```

#### `POST localhost:5000/servicerequests`
- Creates a new servicerequest
- Returns success value, total servicerequests and ID of newly created servicerequest

Header:
| Key             | Value                 | Description                     | Required / Optional         |
|:----------------|:----------------------|:--------------------------------|:----------------------------|
| Content-Type    | application/json      | Payload is in JSON format       | Required                    |
| Authorization   | Bearer &lt;token&gt;  | Requires JWT bearer token       | Required                    |

**Body:**
```
{
    "origin_airport": "Universitaetsklinik Innsbruck",
    "destination_airport": "Klinikum Grosshadern",
    "payload": "Kidney",
    "payload_weight": "5",
    "priority": true,
    "collection_datetime": "2020-05-28 11:30:00",
    "delivery_datetime": "2020-05-28 12:30:00",
    "latest_delivery_datetime": "2020-05-28 13:30:00"
}
```
Response:
```
{
  "created": 4,
  "success": true,
  "total_servicerequests": 4
}
```

#### `PATCH localhost:5000/servicerequests/<int:id>`
- *Updates* servicerequest status
- Returns success value, new servicerequest status and servicerequest ID

Header:
| Key             | Value                 | Description                     | Required / Optional         |
|:----------------|:----------------------|:--------------------------------|:----------------------------|
| Content-Type    | application/json      | Payload is in JSON format       | Required                    |
| Authorization   | Bearer &lt;token&gt;  | Requires JWT bearer token       | Required                    |

Response:
``` 
{
  "status": "Scheduled",
  "success": true,
  "updated_servicerequest_id": 1
}
```

#### `DELETE localhost:5000/servicerequests/<int:id>`

- Deletes servicerequest
- Returns success value, deleted servicerequest ID and number of servicerequests

Header:
| Key             | Value                 | Description                     | Required / Optional         |
|:----------------|:----------------------|:--------------------------------|:----------------------------|
| Authorization   | Bearer &lt;token&gt;  | Requires JWT bearer token       | Required                    |

Response:
```
{
  "deleted_servicerequest_id": 1,
  "success": true,
  "total_servicerequests": 2
}
```

## Testing
To run the tests, run
```
dropdb servicebroker_test
createdb servicebroker_test
psql servicebroker_test < servicebroker.psql
python test_flaskr.py
```

## JWT Bearer Tokens

**Admin token:**
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNaYmhmV0pkaGpqZ2R3clFqR1l0aCJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktZnNuZC5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwMWFiODc3NjAwNDQwMDEzOTlmMWYxIiwiYXVkIjoic2VydmljZXJlcXVlc3QiLCJpYXQiOjE1OTQzNzg3NTUsImV4cCI6MTU5NDQ2NTE1NSwiYXpwIjoiTUVZdU1jMEtlYUNQWll5MXlJdElFMDZIS2htTmV2YTkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpzZXJ2aWNlcmVxdWVzdCIsImdldDpob3NwaXRhbHMiLCJnZXQ6c2VydmljZXJlcXVlc3RzIiwicGF0Y2g6c2VydmljZXJlcXVlc3QiLCJwb3N0OnNlcnZpY2VyZXF1ZXN0Il19.De2ykyMFxoUrPSLqs_AgnAoiuR7dOgFwLmunS6tLs6LGIies2ZTJKovv-EHJpL0R2sx54U-O0IXSuAYIN63Zjinl13S6dBmF1xDgGHhPZKSd96Np4AxPklNGzw3jCjD3I7TbGoXGuYF6TTZNwGR3M6OYL5PBHVc5O-gpt78IbAmVTHmWpqTXdP6oc4d_mb4Pn5yRlnALc1LmzXT7u0y7NhOyk8Q5V6PptEZSevdP9K4yr1Oiwteoiy4lRAe-b0cMATiM18x3GyZkaKAFBXIWNUFCfp-4ZYlMXlxJ_9quU1PhbpXjeXV70CTcCF_AkY-uSH31AJT5dbi25XnWKnXA6A
```

**Client token:**
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNaYmhmV0pkaGpqZ2R3clFqR1l0aCJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktZnNuZC5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwNmUwYjU2YjI1NjEwMDE5MTNkMjAwIiwiYXVkIjoic2VydmljZXJlcXVlc3QiLCJpYXQiOjE1OTQzNzg5NDYsImV4cCI6MTU5NDQ2NTM0NiwiYXpwIjoiTUVZdU1jMEtlYUNQWll5MXlJdElFMDZIS2htTmV2YTkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpob3NwaXRhbHMiLCJwb3N0OnNlcnZpY2VyZXF1ZXN0Il19.6Ye0CNXChkNVG2chpvbyJ-oUNInLIp437bAcuE3bAC_v1Vi-IXZjS8q5XxR1FXvBdQ9BWt9xlsWXJB1UCCUuDe3YNOyF5zwmOG9VxKfaYRNBu_uTRXdeAKknSKkcxQ9mHd7aKKGL2SInvDwBSGplO6st3w65rNO5XXnLOTNS4XqNHAG6-U7BbFr0Q2xC2af4IPteBCLnDj7fghGzr5nz7p_urcC1i5346n7gPPeTbTZEd_Tzt-XjBQU-zigmnE5eycKzUjdNtUMdWzApgmV6WeFaOUMb1UScmYwT9mqHwZwa-8j9kKhIPUFpXa88NTIeAJKpxBW5_kenJTIZ7aBD2g
```
