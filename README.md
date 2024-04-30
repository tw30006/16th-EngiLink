## Setup

### Frontend

- install `node` and `npm`
- run `npm install` to install necessary packages.
- run `npm run dev` to start the frontend server.

### Backend

- install Python and package manager `poetry` via `pipx install poetry`
- run `poetry shell` to enter or activate the virtual environment.
- then run `poetry install` to install necessary packages.
- run `python manage.py migrate` to apply migrations if necessary.
- run `python manage.py runserver` to start the server.
- visit `http://localhost:8000` to see the app.