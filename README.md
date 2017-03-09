### Installation

    git clone https://github.com/cscanlin/films_api.git
    cd films_api
    pip install -r requirements.txt
    python manage.py migrate

### Running

    python manage.py runserver

Then got to http://127.0.0.1:8000/

### About

This project is built with Django and heavily leverages the django-rest-framework.

The API logic is stored in 4 main parts:

1. `models.py` - Defines the Film and Ranking models and their (typed) attributes. Also holds the logic for loading the sample data from json.
