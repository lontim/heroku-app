To create new tokens, use the following URL:
https://tim-eu.eu.auth0.com/authorize?audience=agency&response_type=token&client_id=a43SpbN7ZUcEKx5Ck7a2YX8im4IYL4H3&redirect_uri=http://localhost:8080/login-results

# Udacity full stack web developer (FSWD) - Capstone Project
# Subject: Casting Agency

## Overview

The application allows management of actors and films. According to a users' roles and privileges, they will have different capabilities.
These vary, so for example, a Casting Assistant will be able to view films and actors, while a Casting Director can edit films, add and
remove actors. An API is exposed, which interfaces with a Postgres relational database. The following tables are used:

* actor
* film
* film_actors
 
## Technical details

* Python and the Flask framework
* PostgreSQL relational database management system (RDBMS)
* Alembic for database migrations
* Heroky by Salesforce
* Auth0 for login, authentication and authorisation capabilities

## Local environment for running the project

1. Create a Python Virtual Environment

```bash
python3 -m venv myvenv
```

2. Activate the Virtual Environment

```bash
source myvenv/bin/activate
```

3. Install the dependancies called out in the `requirements.txt`

```bash
pip install -r requirements.txt
```

## Authentication

Fresh access tokens can be generated using Auth0.

Hyperlink: https://tim-eu.eu.auth0.com/authorize?audience=agency&response_type=token&client_id=a43SpbN7ZUcEKx5Ck7a2YX8im4IYL4H3&redirect_uri=http://localhost:8080/login-results

