# Discount Manager

Service provides API for managing discount codes.

### Install
Service is written with Python 3.10. Pipfile has all necessery dependencies. For installation run
```
pipenv run install
```

Setting for Postgres should be specified in environment. Environment variables example can be found in .env file.

### Database Migration
Migration is done using Alembic.
```
pipenv run migrate
```

### Run app
```
pipenv run api
```

### Available Endpoints
```
POST /api/{brand_id}/discount/generate
GET /api/{brand_id}/discount/fetch?user_id={user_id}
```

![Diagram](https://github.com/rybach/discount_server/blob/main/images/diagram.drawio.svg)
