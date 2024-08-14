# URL Shortener API

This project implements a basic URL shortener API using FastAPI and PostgreSQL. It provides two main endpoints:

1. `POST /shorten`: Accept a long URL and return a shortened URL
2. `GET /{short_code}`: Redirect to the original URL

## Prerequisites

- Python 3.7+
- PostgreSQL
- pip (Python package manager)

## Setup

1. Clone the repository:

   ```
   git clone https://github.com/naresh1219990/url-shortener-api.git
   cd url-shortener-api
   ```

2. Create a virtual environment and activate it:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```
   pip install fastapi[all] sqlalchemy psycopg2-binary shortuuid
   ```

4. Set up your PostgreSQL database and update the `SQLALCHEMY_DATABASE_URL` in `main.py` with your database credentials.

5. Run the application:
   ```
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`.

## API Usage

### Shorten a URL

To shorten a URL, send a POST request to `/shorten`:

```
curl -X POST "http://localhost:8000/shorten" -H "Content-Type: application/json" -d '{"url": "https://www.example.com/very/long/url"}'
```

The response will contain the shortened URL:

```json
{
  "shortened_url": "http://localhost:8000/abcd1234"
}
```

### Redirect to Original URL

To use a shortened URL, simply open it in a web browser or send a GET request:

```
curl -L "http://localhost:8000/abcd1234"
```

This will redirect to the original URL.

## Project Structure

- `main.py`: The main FastAPI application file containing all the routes and database models.

## Database Schema

The project uses a simple database schema with a single table:

```sql
CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    original_url TEXT NOT NULL,
    short_code VARCHAR(8) UNIQUE NOT NULL
);
```
