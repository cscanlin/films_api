See it live: https://films-api.herokuapp.com/

### Installation

    git clone https://github.com/cscanlin/films_api.git
    cd films_api
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py loaddata test_data

You will also need to set an environment variable for `FILMS_API_SECRET`

### Running

    python manage.py runserver

Then got to http://127.0.0.1:8000/

### About

This project is built with Django and heavily leverages the django-rest-framework.

Full endpoint docs are available at: https://films-api.herokuapp.com/docs

The API logic is split among 4 main parts:

1. `models.py` - Defines the Film and Ranking models and their (typed) attributes. Also holds the logic for loading the sample data from json.

2. `serializers.py` - Controls which fields should be pulled from each model, including logic with dynamic fields. Also handles any nesting functionality.

3. `views.py` - Contains classes which dispatch and execute all CRUD logic. Also handles all of the filtering logic.

4. `urls.py` - Defines the routes and connects matching view/controller functionality.

The django-rest-framework is useful because it removes much of the boilerplate associated with a standard django rest app, and makes it extremely easy to add the full list of http verbs to each endpoint. It also makes it easy to add useful features like pagination, filtering, and ordering, that can be fully customized based on each use case.

One other nice feature of django-rest, is that when you go to the api routes in a web browser, you will see a convenient browsable API with widgets for making requests, and controlling filters and ordering. This response is controlled by the request headers, and only returns the browsable view if the `Accept` header is set to `text/html` (which most browser have by default). I have also included an additional library that makes full endpoint documentation based on code structure (Available at https://films-api.herokuapp.com/docs)

The application is deployed on a free heroku instance as well, and can be viewed live at: https://films-api.herokuapp.com/

### Tests

Tests are in `tests.py` and can be run with:

    python manage.py test


### TODO
  - better nested serializer/route handling
  - PropTypes
  - control fields present in serializer (replace __all__)
  - True NEST_LEVEL??
  - Full OpenApi3 w/ nested schema and $ref
