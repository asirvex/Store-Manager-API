[![Build Status](https://travis-ci.org/asirvex/Store-Manager-API.svg?branch=develop)](https://travis-ci.org/asirvex/Store-Manager-API)
[![Coverage Status](https://coveralls.io/repos/github/asirvex/Store-Manager-API/badge.svg?branch=ft-get-one-sale-161391183)](https://coveralls.io/github/asirvex/Store-Manager-API?branch=ft-get-one-sale-161391183)
[![Maintainability](https://api.codeclimate.com/v1/badges/3d36e6e1f288e7eb8f9e/maintainability)](https://codeclimate.com/github/asirvex/Store-Manager-API/maintainability)

Heroku link https://asava-store-manager.herokuapp.com/

Steps to run the project

* Create a virtual environment with the command
  `$ virtualenv -p python3 env`

* Activate the env with the command
`$ source env/bin/activate`

* Install git

* clone this repo

* cd into the folder Store-Manager-API

* install requirements
`$ pip install -r requirements.txt`
* export required enviroments

`$ export SECRET_KEY="anysecretkey"`

`$ export APP_SETTINGS="development"`

`$ export FLASK_APP="run.py"`

* Now you can run
  * for the application run
  `$ flask run`
  * for tests
  `$ nosetests`

* Test the endpoints using postman

Endpoint | Functionality | Requirements
------------ | ------------- | -------------
post /api/v2/auth/signup | register a user | user information
post /api/v2/auth/login | get sales | password authentification
get /api/v2/products | view all the products | access_token
post /api/v2/products | creates a new product entry | product info, access_token
get /api/v2/products/<int> | get one product | access_token
get /api/v2/sales | get sales | access_token
get /api/v2/sales/<int>| get one sale | access_token
post /api/v2/sales | create a new sale entry | sale info, access_token
