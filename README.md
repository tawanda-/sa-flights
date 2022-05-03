<p align="center" style="font-weight: 300;font-size: 5em;"><img src="https://github.com/tawanda-/sa-flights/blob/master/frontend/src/logo.jpeg" alt="logo" width=20%/>SA Flight Tracker</p>

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

- View statistical flight data for the different airports

- Admin panel to manage data

## Tech

SA Flight Tracker is comprised of a backend server that stores the flight data and a website for displaying the data.

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


### From Source

#### Backend

[Python 3+] is required to run the application and its best to create a venv for the application.

Clone the repo and activate a python vrtual environment

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

After all the packages have been installed, we need to setup Django. The following command will run migrations, load initial data into the database, create a superuser and then start the server

```
./setup.sh
```

### Docker

- The following commands will clone the repo and initialise the docker container

  ```
  git clone https://github.com/tawanda-/sa-flights
  cd sa-flights
  docker-compose up
  ```

To test the server you can go to:

- [Admin panel](127.0.0.1/admin) enter the superuser username and password.
- [GraphQL API](127.0.0.1/grapqhl) to test the api

### Testing

To test backend source code, in the backend folder type the following command into your terminal

```
python manage.py test saflightsapi.tests
```

## License

MIT
