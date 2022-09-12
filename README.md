# Code Challenge Template

## Introduction
This is Thomas O'Brien's submission for the mid-level engineering position as a Remote Colaberry Consultant for Corteva Agriscience's Field Solutions Data Team.
This repo contains the code for a data pipeline with the capabilities to ingest local text files with weather and crop yield data, perform basic analytics, and return paginated data via REST APIs.

## Getting Started
- Basic Requirements: pip, git, and python>=3.7 working on your machine
- Clone this repo
  - `git clone https://github.com/tobrien502/code-challenge-template`
  - `cd code-challenge-template`
- Create and activate a virtual environment
  - `python3 -m venv <venv_name>`
  - `source <venv_name>/bin/activate`
- Install required Python packages
  - `pip install -r requirements.txt`
- Set Django settings
  - `cd src/pipeline`
  - `export DJANGO_SETTINGS_MODULE="pipeline.settings"`
- Create database tables locally
  - `python3 manage.py migrate`
- Create a superuser
  - `python3 manage.py createsuperuser`
  - Enter username, email, and password

## Testing
- Execute the following command to run all tests across all apps within the project:
  - `pytest .`

## Using the Admin Pages
- Start your local server
  - `python3 manage.py runserver`
- Paste the following url in your browser
  - `http://127.0.0.1:8000/admin/`
- Login with the superuser creds you just created
- Here you will have full CRUD abilities for all models

## Data Ingestion
- In order to load data, txt files containing weather or yield data must be located in either `code-challenge-template/wx_data` or `code-challenge-template/yld_data` respectively.
- Execute the following command to load weather data
  - `python manage.py import_data --weather`
- Execute the following command to load yield data
  - `python manage.py import_data --yield`
- Both of the above commands will turn all lines in the txt files in database records using Pandas and the Django ORM. Log output will be structured as seen below:
  - `Starting ingestion of yield data from the txt files in the yld_data folder at 2022-09-12 00:50:07.536960.`
  - `Done processing file: US_corn_grain_yield.txt`
  - `Finished importing data at 2022-09-12 00:50:07.552250. Records loaded: 30 Records failed: 0`
- There is a unique constraint on the CropData model for the year field and the pair of station_id and date are unique for the WeatherData model. If an Integrity Error is encountered then that record is not created.

## Data Analysis
- 


