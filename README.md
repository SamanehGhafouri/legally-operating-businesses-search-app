# About Search App (Legally Operating Businesses)

A RESTful API with user-friendly endpoints seamlessly exposed through Swagger documentation. This project is centered around leveraging data sourced from NYC Open Data, specifically focusing on legally operating businesses. By meticulously populating the database with this dataset, the API efficiently delivers valuable insights. Users can effortlessly access information on businesses, including their active or inactive license status during specified timeframes.

# Search App Tech Stack
Search App is built in `Python` using `Django Rest Framework`, `PostgreSQL`, and containerized with `Docker`.

# Requirements to Run
1. Have [Docker](https://docs.docker.com/desktop/) installed on your machine.
2. Add `.env.dev` file to the root of the project and copy/paste the content of `sample.env.dev` file into `.env.dev`.
3. cd into `app` and run `docker build .` to build the project.
4. cd `..` then run `docker-compose up`.
5. run `docker-compose run web python manage.py loaddata business.json` to populate the database with the data stored in the fixture `business.json`.
6. Open the web browser and paste `http://localhost:8000/api/docs/` where all the endpoints are documented via `Swagger`.