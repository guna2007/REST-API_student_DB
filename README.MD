# Student API (FastAPI)

A simple, production-style REST API for managing students, built with FastAPI and tested with pytest. The service keeps data in-memory (no database) and exposes endpoints for create, read, update, and delete (CRUD) operations.

## Features

- **FastAPI**: High-performance Python web framework
- **Pydantic v2**: Request/response data validation
- **Swagger UI**: Interactive API docs at `/docs`
- **pytest**: Automated tests for all endpoints
- **In-memory store**: No external database required

## Tech Stack

- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Validation**: Pydantic (>=2)
- **Server**: Uvicorn (ASGI)
- **Testing**: pytest, httpx/TestClient

## Project Structure

```
student-api/
├─ app/
│  ├─ __init__.py
│  └─ main.py           # FastAPI app with routes and in-memory store
├─ tests/
│  └─ test_students.py  # Pytest test cases for all endpoints
├─ requirements.txt      # Dependencies
└─ README.md             # Project documentation
```

## Getting Started

1. **Create a virtual environment**

   - macOS/Linux:
     ```bash
     python -m venv .venv
     source .venv/bin/activate
     ```
   - Windows (PowerShell/CMD):
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the API server**
   ```bash
   uvicorn app.main:app --reload
   ```
   - Visit: http://127.0.0.1:8000/docs for Swagger UI

## Data Models

- **StudentCreate (request body for create)**

  - `name` (str): 2–50 chars
  - `age` (int): 13–24
  - `grade` (int): 5–10

- **Student (response)**
  - `id` (int)
  - `name` (str): Title-cased automatically (e.g., "sai" -> "Sai")
  - `age` (int)
  - `grade` (int)

## API Reference

- **GET** `/` — Health check

  - Response: `{ "working": "Good" }`

- **POST** `/students` — Create a new student

  - Body (JSON): `{ "name": "Guna", "age": 18, "grade": 9 }`
  - 201 Created → `Student`

- **GET** `/students` — List/search students

  - Query params (all optional):
    - `min_age` (int, >=13)
    - `grade` (int, >=5)
    - `search` (str, substring match in name)
  - 200 OK → `Student[]`
  - 404 Not Found if no students match filters

- **GET** `/student/{id}` — Get student by ID

  - Path: `id` (int, >=1)
  - 200 OK → `Student`
  - 404 Not Found with detail `"Data not Found {id}"`

- **DELETE** `/student/{id}` — Delete student by ID

  - 200 OK → `{ "{id}": "deleted" }`
  - 404 Not Found with detail `"ID not found"`

- **PUT** `/student/{id}` — Update student by ID (via query params)
  - Query params (all optional): `name` (str), `age` (13–24), `grade` (5–10)
  - 200 OK → Updated `Student`
  - 404 Not Found with detail `"ID not Found"`
  - 422 Unprocessable Entity for invalid query values

## Using Swagger UI (/docs)

Follow these steps to explore and test the API using the built-in Swagger UI:

1. Start the server and open http://127.0.0.1:8000/docs in your browser.
2. Expand an endpoint, click "Try it out", fill required fields, then click "Execute".

### Walkthrough

- GET `/` — Health check

  - Expand "GET /" → Try it out → Execute
  - You should see `{ "working": "Good" }` in the Response body.

- POST `/students` — Create a new student

  - Expand "POST /students" → Try it out
  - In the Request body, enter:
    ```json
    { "name": "GUna", "age": 18, "grade": 9 }
    ```
  - Execute → Expect 201 Created with a response containing `id` and title-cased `name` (e.g., "Guna").

- GET `/students` — List/search students

  - Expand "GET /students" → Try it out
  - Leave all query params empty to list all
  - Optionally set filters:
    - `min_age` (>= 13)
    - `grade` (>= 5)
    - `search` (substring match in name)
  - Execute → 200 with a list of students, or 404 if no results match.

- GET `/student/{id}` — Get student by ID

  - Expand → Try it out → Enter `id` (>= 1) → Execute
  - Expect 200 with the student or 404 with detail `"Data not Found {id}"`.

- PUT `/student/{id}` — Update student by ID

  - Expand → Try it out
  - Enter `id` and any of the optional query params: `name`, `age` (13–24), `grade` (5–10)
  - Execute → 200 with the updated student, or 404 if ID not found.

- DELETE `/student/{id}` — Delete student by ID
  - Expand → Try it out → Enter `id` → Execute
  - Expect 200 with `{ "{id}": "deleted" }`, or 404 if ID not found.

### Validation

- Invalid inputs return 422 with details (e.g., too-short name, out-of-range age/grade).
- Names are normalized to Title Case on create and update.

## Running Tests

```bash
pytest -q
```

## Notes & Limitations

- **In-memory store**: Data resets when the server restarts.
- **Empty searches**: `/students` returns 404 when no students match filters.
- **Name normalization**: Names are title-cased on create and update.
- **PUT body**: Update is done via query parameters, not JSON body.

## License

This project is for learning purposes. Choose and add a license if you plan to distribute.
