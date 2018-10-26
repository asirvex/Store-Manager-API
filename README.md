[![Build Status](https://travis-ci.org/asirvex/Store-Manager-API.svg?branch=develop)](https://travis-ci.org/asirvex/Store-Manager-API)
[![Coverage Status](https://coveralls.io/repos/github/asirvex/Store-Manager-API/badge.svg?branch=develop)](https://coveralls.io/github/asirvex/Store-Manager-API?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/8c5bc842bc44fc7b1e26/maintainability)](https://codeclimate.com/github/asirvex/Fast-Food-API/maintainability)

Heroku link https://asava-store-manager.herokuapp.com/

Steps to run the project

1. Create a virtual environment with the command
  `$ virtualenv -p python3 env`

1. Activate the env with the command
`$ source env/bin/activate`

1. Install git

1. clone this repo

1. cd into the folder Store-Manager-API

1. install requirements
`$ pip install -r requirements.txt`

1. export required enviroments

`$ export SECRET_KEY="anysecretkey"`
`$ export APP_SETTINGS="development"`
`$ export FLASK_APP="run.py"`

1. Now you can run


  11. for the application run
  `$ flask run`

  11. for tests
  `$ nosetests`

1. Test the endpoints using postman

Endpoint | Functionality | Requirements
------------ | ------------- | -------------
post /api/v1/auth/signup | register a user | user information
post /api/v1/auth/login | get sales | password authentification
get /api/v1/products | view all the products | access_token
post /api/v1/products | creates a new product entry | product info, access_token
get /api/v1/products/<int> | get one product | access_token
get /api/v1/sales | get sales | access_token
get /api/v1/sales/<int>| get one sale | access_token
post /api/v1/sales | create a new sale entry | sale info, access_token
