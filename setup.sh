#!/bin/bash
export DATABASE_URL="postgresql://tim@localhost:5432/capstone"
export FLASK_APP="app.py"
export AUTH0_DOMAIN="tim-eu.eu.auth0.com"
export API_AUDIENCE="agency"
export AUTH0_CALLBACK_URL="http://0.0.0.0:8080" 
