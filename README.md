# HRMS Lite API

A lightweight **Human Resource Management System (HRMS)** backend built with FastAPI. It provides REST APIs to manage employees and track their daily attendance.

---

## Project Overview

HRMS Lite exposes a versioned REST API (`/api/v1`) with two core modules:

- **Employees** – Create, list, and delete employee records.
- **Attendance** – Mark and retrieve attendance entries per employee, with date-range filtering and an aggregate summary report.

The project is production-ready with:
- MySQL database (hosted on [Aiven](https://aiven.io)) with SSL enforcement
- CORS configured for specific frontend origins
- Auto table creation on startup via SQLAlchemy
- Interactive API docs at `/docs` (Swagger UI)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.13 |
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Database | MySQL (Aiven Cloud) |
| DB Driver | PyMySQL |
| Validation | Pydantic v2 |
| Config | pydantic-settings (`.env` file) |
| Server | Uvicorn (ASGI) |
| Deployment | Render (backend) |

---

## Project Structure

```
ethera_hrms_backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── employees.py     # Employee route handlers
│   │       └── attendance.py    # Attendance route handlers
│   ├── core/
│   │   ├── config.py            # App settings (loaded from .env)
│   │   └── database.py          # SQLAlchemy engine & session
│   ├── models/
│   │   ├── employee.py          # Employee DB model
│   │   └── attendance.py        # Attendance DB model
│   ├── schemas/
│   │   ├── employee.py          # Pydantic schemas for Employee
│   │   └── attendance.py        # Pydantic schemas for Attendance
│   └── main.py                  # App entry point, CORS middleware
├── .env                         # Local environment variables (not committed)
├── env.example                  # Template for .env
├── requirements.txt
└── README.md
```

---

## API Endpoints

Base URL: `/api/v1`

### Employees

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/employees/` | Create a new employee |
| `GET` | `/employees/` | List all employees |
| `DELETE` | `/employees/{employee_id}` | Delete employee by employee_id |

**Employee fields:** `employee_id` (unique string), `full_name`, `email` (unique), `department`

### Attendance

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/attendance/` | Mark attendance for a given day |
| `GET` | `/attendance/` | List attendance (filterable by `employee_id`, `start_date`, `end_date`) |
| `GET` | `/attendance/summary` | Get total present-days count per employee |

**Attendance fields:** `employee_id` (int FK), `date` (YYYY-MM-DD), `status` (`Present` or `Absent`)

---

## Running the Project Locally

### Prerequisites

- Python 3.10+
- A MySQL database (local or cloud, e.g. Aiven)

### 1. Clone the repository

```bash
git clone <repo-url>
cd ethera_hrms_backend
```

### 2. Create and activate a virtual environment

```bash
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# macOS / Linux
python -m venv .venv
source .venv/bin/activate
```

> If PowerShell blocks script execution, run:
> `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example file and fill in your values:

```bash
cp env.example .env
```

Edit `.env`:

```env
PROJECT_NAME="HRMS Lite API"
DATABASE_URL="mysql+pymysql://<user>:<password>@<host>:<port>/<database>"
API_V1_STR="/api/v1"
```

> **Aiven users:** Copy the exact host from your Aiven Console → your MySQL service → Connection information. SSL is already enforced in `database.py` via `connect_args`.

### 5. Run the development server

```bash
uvicorn app.main:app --reload
```

The API will be available at: **http://127.0.0.1:8000**

Interactive docs: **http://127.0.0.1:8000/docs**

---

## Deployment

| Service | URL |
|---|---|
| Backend (Render) | `https://ethera-hrms-backend.onrender.com` |
| Frontend (Vercel) | `https://ethera-hrms-frontend-4oq2rgnlw-aishwarys-projects-aa3b0a85.vercel.app` |

### Environment Variables on Render

Set the following in Render → your service → **Environment**:

```
PROJECT_NAME=HRMS Lite API
DATABASE_URL=mysql+pymysql://<user>:<password>@<host>:<port>/<database>
API_V1_STR=/api/v1
```

---

## Assumptions & Limitations

| # | Item |
|---|---|
| 1 | **Attendance is one record per employee per day** — duplicate entries for the same employee on the same date are rejected with HTTP 400. |
| 2 | **No authentication** — all endpoints are publicly accessible. Auth (JWT/OAuth2) is not implemented. |
| 3 | **Attendance status** is limited to `Present` or `Absent` only. |
| 4 | **Employee deletion is cascading** — deleting an employee also removes all their attendance records. |
| 5 | **Tables are auto-created** on startup via `Base.metadata.create_all()`. No migration tool (e.g. Alembic) is used. |
| 6 | **CORS** is configured for specific frontend origins. If the frontend URL changes, update the `origins` list in `app/main.py`. |
| 7 | **Aiven free-tier** may enforce IP allowlisting — add your server's IP in Aiven Console → Overview → Allowed IP Addresses if connections are refused. |

---

## .gitignore Note

The `.env` file is already included in `.gitignore`. **Never commit your `.env`** as it contains database credentials.
