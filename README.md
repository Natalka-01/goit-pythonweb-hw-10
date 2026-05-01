# FastAPI Contacts Management API

This is a REST API for managing contacts built with FastAPI and SQLAlchemy.

## Features

- CRUD operations for contacts
- Search contacts by name, surname, or email
- Get contacts with birthdays in the next 7 days
- PostgreSQL database
- Pydantic validation
- Swagger documentation

## Setup

1. Start the PostgreSQL container:

```bash
docker run --name goit-postgres -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure connection if necessary:

- By default, `postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/postgres` is used
- For custom password, set `DATABASE_URL`

4. Run migrations:

```bash
alembic upgrade head
```

5. Populate the database:

```bash
python seed.py
```

## Run the application

```bash
uvicorn main:app --reload
```

## API Endpoints

- GET /contacts - Get all contacts (with pagination: skip, limit)
- GET /contacts/{contact_id} - Get contact by ID
- POST /contacts - Create new contact
- PUT /contacts/{contact_id} - Update contact
- DELETE /contacts/{contact_id} - Delete contact
- GET /contacts/search/?query={search_term} - Search contacts by name, surname, or email
- GET /contacts/birthdays/ - Get contacts with birthdays in the next 7 days

## Swagger Documentation

After starting the server, visit `http://localhost:8000/docs` for interactive API documentation.
