# ems_system_be
python django rest framework 

# Django REST Framework Backend

A backend REST API built using **Django** and **Django REST Framework (DRF)**.  
This project provides a clean, scalable API structure suitable for frontend integration and production use.

---

## 🚀 Tech Stack

- 🐍 Python
- 🌐 Django
- 🔗 Django REST Framework
- 🔐 JWT Authentication
- 📦 pip / virtualenv

---

## 📁 Project Structure

backend/
├── api/
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ ├── urls.py
│ └── admin.py
│
├── config/
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
│
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md


---

## ⚙️ Prerequisites

- Python ≥ 3.10
- pip
- virtualenv (recommended)

---

## 📦 Installation

Create and activate virtual environment:

```bash

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

🗄️ Database Setup

Run migrations:

python manage.py makemigrations
python manage.py migrate

Create superuser:

python manage.py createsuperuser

▶️ Run Development Server

python manage.py runserver


Server will run at:

http://127.0.0.1:8000/

🔐 Authentication

JWT-based authentication

Obtain token:

POST /api/token/


Refresh token:

POST /api/token/refresh/

📌 API Endpoints (Example)
GET    /api/employees/
POST   /api/employees/
GET    /api/employees/{id}/
PUT    /api/employees/{id}/
DELETE /api/employees/{id}/
