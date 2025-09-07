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

## Examples

- Create a student

  ```bash
  curl -X POST http://127.0.0.1:8000/students \
       -H "Content-Type: application/json" \
       -d '{"name":"GUna","age":18,"grade":9}'
  ```

- List all students

  ```bash
  curl http://127.0.0.1:8000/students
  ```

- Filter by age and grade

  ```bash
  curl "http://127.0.0.1:8000/students?min_age=17&grade=9"
  ```

- Search by name substring

  ```bash
  curl "http://127.0.0.1:8000/students?search=a"
  ```

- Get by ID

  ```bash
  curl http://127.0.0.1:8000/student/1
  ```

- Update by ID (query params)

  ```bash
  curl -X PUT "http://127.0.0.1:8000/student/1?name=maDHan&age=21&grade=8"
  ```

- Delete by ID
  ```bash
  curl -X DELETE http://127.0.0.1:8000/student/1
  ```

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

---

Tip: A repo info file for this workspace is missing (`.zencoder/rules/repo.md`). If you want, I can generate it to improve future assistance quality.
