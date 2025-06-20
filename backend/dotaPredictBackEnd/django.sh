#!/bin/bash
echo "Create migrations"
python manage.py makemigrations predictionapp
python manage.py makemigrations userapp
python manage.py makemigrations matchapp
python manage.py makemigrations heroapp
echo "==============="

echo "Migrate"
python manage.py migrate
echo "==============="

echo "Start server"
python manage.py runserver 0.0.0.0:8000