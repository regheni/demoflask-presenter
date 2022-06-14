How to run?
Set up your venv

`virtualenv venv`

Install requirements
`pip install -r requirements.txt`

Install current package in debug mode
`pip install -e .`

Set env vars for flask
`export FLASK_APP=app;
export FLASK_ENV=development`

Run the alembic (db) migrations:
`alembic upgrade head`

Move current dir:
`cd src/presenter`

Run flask
`flask run`

