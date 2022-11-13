#!/bin/bash
export DATABASE_URL="postgresql://tim@localhost:5432/capstone"
export FLASK_APP="app.py"
export AUTH0_DOMAIN="tim-eu.eu.auth0.com"
export API_AUDIENCE="agency"
export AUTH0_CALLBACK_URL="http://0.0.0.0:8080" 

export CASTING_ASSISTANT_TOKEN=""
export CASTING_DIRECTOR_TOKEN=""
export EXEC_PRODUCER_TOKEN=""
export ERROR_TOKEN=""