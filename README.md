<p align="center">
	<img src="https://github.com/tawanda-/sa-flights/blob/master/frontend/src/logo.svg" alt="logo" width=10%/>
	<h2 align="center">SA Flight Tracker</h2>
</p>

<p align="center">
	<img src="https://img.shields.io/badge/django-v3.2.12+-green" alt="django" />
	<img src="https://img.shields.io/badge/react-v17.0.2+-blue.svg" alt="react" />
</p>

<p align="center">
	SA Flights Tracker is a website to monitor flights flying into and out of 21 airports in South Africa
</p>

<p align="center">
	<a href="#features">Features</a> •
	<a href="#tech">Tech</a> •
	<a href="#installation">Installation</a> •
	<a href="#license">License</a> •
</p>

## Features

- View real time flight data as well as historical(24 hours) data for a given airport.

- Search for flights using 

  - Airport name,
  - ICAO, IATA flight or airport number,
  - Departure city and/or Arrival City

- Admin panel to manage data

## Tech

SA Flight Tracker is comprised of a Django backend server that stores the flight data and a react website for displaying the data.

### Backend

[Django](https://www.djangoproject.com/) For content management through Admin panel that is data quering, storage and presentation to client via the SAFlightsApi.

[Django-Graphene](https://docs.graphene-python.org/projects/django/en/latest/) Used to create Graphql front facing api

[AviationStack](https://aviationstack.com/) Provided flight data. After a user requests flight data, if the data is not available in the app, Django requests the data from Aviationstack and stores the data. The aviationstack api has a quota of 100 calls

### FrontEnd

[React](https://reactjs.org/) Used to create the single page application.

[Apollo Client](https://www.apollographql.com/docs/react/) Used to make grapqhl data requests to SA Flights Tracker APi

[Bootstrap](https://getbootstrap.com/) Make the website look pretty

### Api

The SAflightsapi is accesible using the following link 

```
{url}/graphql
```

## Installation

### Airlabs Api Key

The appplication uses airlabs.co as the source of flight data.
To get the api key go to the [sign up](https://airlabs.co/signup) page, fill in the details save the key it will be used by the backend to request flight data.

### From Source

#### 1. Backend

##### RabbitQM

[download](https://www.rabbitmq.com/download.html) and install rabbitqm

##### Django

[Python 3+] is required to run the application and its best to create a venv for the application.

Clone the repo and activate a python virtual environment

```
git clone https://github.com/tawanda-/sa-flights
cd sa-flights
python3 -m venv env
source env/bin/activate
```

This will activate the virtual environment.

The following commands will install the required packages

```
cd backend
pip install -r requirements.txt 
```

##### Django Setup

In myproject/settings update the AIRLABS_KEY with your key.

After all the packages have been installed, we need to setup Django. The following command will run migrations, load initial data into the database, create a superuser, start celery and also start Django test server

```
./setup.sh
```

##### Testing

To test backend source code, in the backend folder type the following command into your terminal

```
python manage.py test saflightsapi.tests
```

#### 2. Frontend

In terminal run the following commands

```
cd frontend
npm install
npm start
```

In browser enter 127.0.0.1:3000 to view website.

### Using Docker

The following commands will clone the repo and initialise the docker container

```
git clone https://github.com/tawanda-/sa-flights
cd sa-flights
In myproject/settings update the AIRLABS_KEY with your key.
docker-compose up
```

To test the server you can go to:

- Admin panel 127.0.0.1:8000/admin enter the superuser username and password.
- GraphQL API 127.0.0.1:8000/grapqhl to test the api
- Website 127.0.0.1:3000 to view the website

## License

MIT
