# Stringing Manager

#### Video Demo


#### Description
This is an application for management stringings data.

In Tennis the racquets' strings often break from an instensive play and need to be replaced - a process called "
stringing".

This application was created for a person who can restrung tennis racquets. It allows management of:

- Racquets and racquet brands
- Customers, who need their racquets to be restrung
- Stringings per customer
- Payments

It also has a nice dashboard that shows a statistical overview of the data.

## Project Overview

The application is written in [Flask/Python](https://flask.palletsprojects.com/en/2.0.x/) on the server side.

It uses [SQLite](https://www.sqlite.org/index.html) as a database and [SQLAlchemy](https://www.sqlalchemy.org/)
(SQL toolkit and Object Relational Mapper) to access it.

JavaScript is used to display charts on the client side with the help of [Chart.js](https://www.chartjs.org/).

[Bootsrap version 5](https://getbootstrap.com/) is used for styling with
a [dark theme](https://mdbootstrap.com/freebies/dark-theme/).

### Files

`__init__.py`

The project is a Python module and this file has the initialization code for creating the application and a database.
The Flask application uses `flask_login` package for managing user sessions.

`main.py`

Start the Flask application.

`models.py`

Contains definitions of the SQLAlchemy ORM (Object Relational Model) models and relations for each application entity.
They are used to query and alter the database.

`auth.py`

Contains the logic for "sign up" and "login" routes for the application administrators. The password is stored in a hashed
form by using `werkzeug.security` package.

`views.py`

Contains the logic for the application routes:

| Route         | Description                                      |
|---------------|--------------------------------------------------|
| `/`           | home / dashboard                                 |
| `/brands`     | management of racquet brands                     |
| `/racquets`   | management of rackquets                          |
| `/customers`  | managemenrts of customers                        |
| `/stringings` | managements of stringing orders                  |
| `/payments`   | management of customer's payments for stringings |

"management" means: create / edit

`form_helpers.py`

Contains functions for easier reading of form values that are sent from the client via `POST` requests.
For example `form_value_to_string` will retrun `None` if the form values is missing or an empty `string` after
we `strip()` whitespaces.

### `/templates`

Contains jinja2 templates for the application. Each tamplate extends the base `layout.jinja2` and 
corresponds to a specific route.

In several tamplates there are `macro`s used. They are similar to a function in Python and allow for code reuse.
More info on that: https://jinja.palletsprojects.com/en/3.0.x/templates/#template-inheritance.

`index.jinja2` template prepares JavaScript objects with data to be consumed on the client side to render charts.

The rest of the templates render tables with relevant data, while the last row is a `form` that lets the user to
add a new entry to the database.

`stringings.jinja2` also has "Edit" functionality. When hovered over the row there is an "Edit" button shown in 
the last column of that row. Clicking on the button adds enitity's `id` to the query string and on the next render
the app knows to show a form in that row. The user can edit some prepolutated with current data fields and "Save".

### `/styles`
Contains a custom `styles.css` file.

### `/javascript`
Contains custom JavaScript files.
`dashboard.js` is loaded on the Dashboard/Home page. It has functions for rendering a Charts 
(by using Chart.js) and consumes global variables with data that was prepared on the server side.

### `/images`
Contains images used in the application.

### `/bootstrap_dark`
Contains JavaScript and CSS for Bootstrap's dark theme.

## Running The Project

### Install Dependencies

```
pip install -r requirements.txt
```

### Run

```
python main.py
```

Navigate to http://127.0.0.1:5000/