# 📌 Profile Intelligence Service

## 📖 Project Overview

The **Profile Intelligence Service** is a RESTful API that enriches a given name using external data sources and stores structured profile information.

It integrates with three public APIs:

* Genderize → predicts gender
* Agify → predicts age
* Nationalize → predicts nationality

The system processes this data, classifies age groups, and stores results in a database using **UUID v7 identifiers**.

Key features:

* External API aggregation
* Data normalization and enrichment
* Idempotent profile creation
* Filtering support
* Structured JSON responses

---

#  Setup Instructions

## 1. Clone repository

```bash
git clone https://github.com/your-username/profile-intelligence-service.git
cd profile-intelligence-service
```
---
## 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```
---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```
Required packages:

* Django
* djangorestframework
* requests
* django-cors-headers
* uuid6

---
## 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```
---

## 5. Start server
```bash
python manage.py runserver
```

---
# API Endpoints (Exact Paths)

Base URL:

```
/api
``
---
## 🔹 Create Profile
```
POST /api/profiles
```
---
## 🔹 Get All Profiles (with filters)

```
GET /api/profiles
```
Optional query parameters:

* gender
* country_id
* age_group

---
## 🔹 Get Profile by ID

```
GET /api/profiles/{id}
```
---

## 🔹 Delete Profile
```
DELETE /api/profiles/{id}
```

---
# 📌 Example Requests & Responses
---
## 🔹 POST /api/profiles
### Request
```json
{
  "name": "ella"
}
```
---
### Response (201)
```json
{
  "status": "success",
  "data": {
    "id": "b3f9c1e2-7d4a-4c91-9c2a-1f0a8e5b6d12",
    "name": "ella",
    "gender": "female",
    "gender_probability": 0.99,
    "sample_size": 1234,
    "age": 46,
    "age_group": "adult",
    "country_id": "US",
    "country_probability": 0.85,
    "created_at": "2026-04-01T12:00:00Z"
  }
}
```
---
### Idempotent Response (200)
```json
{
  "status": "success",
  "message": "Profile already exists",
  "data": { "...existing profile..." }
}
```
---
## 🔹 GET /api/profiles
### Response (200)
```json
{
  "status": "success",
  "count": 1,
  "data": [
    {
      "id": "uuid",
      "name": "ella",
      "gender": "female",
      "age": 46,
      "age_group": "adult",
      "country_id": "US"
    }
  ]
}
```

---
## 🔹 GET /api/profiles/{id}
### Response (200)
```json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "name": "ella",
    "gender": "female",
    "gender_probability": 0.99,
    "sample_size": 1234,
    "age": 46,
    "age_group": "adult",
    "country_id": "US",
    "country_probability": 0.85,
    "created_at": "2026-04-01T12:00:00Z"
  }
}
```
---
## 🔹 DELETE /api/profiles/{id}
### Response
```
204 No Content
```
---
# 🚀 Deployment URL
Base API URL:

```
https://your-domain.com/api
```

Example:
```
https://your-domain.com/api/profiles
```
---

# ⚠️ Notes

* All timestamps are in **UTC ISO 8601 format**
* All IDs use **UUID v7**
* CORS is enabled for all origins
* External API failures return **502**
* Duplicate names are handled via **idempotency**
