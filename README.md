https://project-todo.liara.run/



# 🚀 Django Todo API


A simple and powerful API for managing daily tasks, built with Django REST Framework.


## ✨ Features

- ✅ Create, read, update and delete tasks (CRUD)
- 🔐 Token-based authentication
- 🌐 CORS configured for frontend
- 📱 Fully RESTful API
- 🚀 Deployed on Railway
- 📄 Auto-generated API documentation

## 🎯 API Endpoints

### Tasks (Todos)

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| `GET` | `/api/todos/` | Get all tasks | Optional |
| `POST` | `/api/todos/` | Create new task | Required |
| `GET` | `/api/todos/{id}/` | Get single task | Optional |
| `PUT` | `/api/todos/{id}/` | Full update task | Required |
| `PATCH` | `/api/todos/{id}/` | Partial update task | Required |
| `DELETE` | `/api/todos/{id}/` | Delete task | Required |

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/register/` | User registration |
| `POST` | `/api/auth/login/` | Login and get token |
| `POST` | `/api/auth/logout/` | Logout |

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- pip
- virtualenv (recommended)

### Installation & Setup

1. **Clone the repository**
```bash
https://github.com/zeynab-gh/todo_list.git
cd django-todo
2.Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
3.Install dependencies
pip install -r requirements.txt
4.Run migrations
python manage.py migrate
5.Create superuser
<<<<<<< HEAD
python manage.py runserver
=======
python manage.py runserver
>>>>>>> ab1a618bfcbdeb3b300cf123ae24832cf0836dd1
