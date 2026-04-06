# Financial Records Management API

A backend system built using FastAPI for managing financial records such
as income and expenses, along with analytics and role-based access
control.

------------------------------------------------------------------------

## Features

-   JWT Authentication (Access + Refresh Tokens)\
-   Role-Based Access Control (Viewer, Analyst, Admin)\
-   CRUD Operations for Financial Records\
-   Filtering (type, category, date range)\
-   Analytics (summary, category-wise, monthly, recent)\
-   Pagination support\
-   Centralized error handling\
-   Modular architecture

------------------------------------------------------------------------

## Tech Stack

-   FastAPI\
-   PostgreSQL\
-   SQLModel / SQLAlchemy\
-   Redis\
-   Alembic

------------------------------------------------------------------------

## Installation

1.  Clone the repository

git clone https://github.com/your-username/your-repo-name.git\
cd your-repo-name

2.  Create virtual environment

python -m venv myenv\
source myenv/bin/activate\
myenv`\Scripts`{=tex}`\activate  `{=tex}

3.  Install dependencies

pip install -r requirements.txt

4.  Setup environment variables (.env)

DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/dbname\
JWT_SECRET_KEY=your_secret_key\
JWT_ALGORITHM=HS256\
REDIS_HOST=localhost\
REDIS_PORT=6379

------------------------------------------------------------------------

## Database Setup (Alembic)

alembic revision --autogenerate -m "initial migration"\
alembic upgrade head

------------------------------------------------------------------------

## Run the Application

uvicorn src.main:app --reload

------------------------------------------------------------------------

## API Documentation

http://localhost:8000/docs\
http://localhost:8000/redoc

------------------------------------------------------------------------

## Authentication Endpoints

POST /api/v1/auth/signup (Public)\
POST /api/v1/auth/login (Public)\
POST /api/v1/auth/refresh (Refresh Token Required)\
GET /api/v1/auth/me (Authenticated)\
GET /api/v1/auth/logout (Authenticated)

------------------------------------------------------------------------

## Financial Endpoints

GET /api/v1/financial/ (Viewer, Analyst, Admin)\
GET /api/v1/financial/transactions/{id} (Viewer, Analyst, Admin)\
POST /api/v1/financial/ (Admin)\
PATCH /api/v1/financial/transactions/{id} (Admin)\
DELETE /api/v1/financial/transactions/{id} (Admin)

------------------------------------------------------------------------

## Analytics Endpoints

GET /api/v1/analytics/summary (Viewer, Analyst, Admin)\
GET /api/v1/analytics/by-category (Viewer, Analyst, Admin)\
GET /api/v1/analytics/monthly (Viewer, Analyst, Admin)\
GET /api/v1/analytics/recent (Viewer, Analyst, Admin)

------------------------------------------------------------------------

## Roles

Viewer: View records\
Analyst: View and analyze data\
Admin: Full access

------------------------------------------------------------------------

## Final Note

This project focuses on clean architecture, scalability, and real-world
backend practices.
