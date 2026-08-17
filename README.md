# PSUSphere

A Django-based student organization management system for organizing and managing colleges, academic programs, student organizations, students, and organization memberships.

## 📌 About the Project

*PSUSphere* is a web application developed using *Django* and *SQLite*. It provides an administrative interface for managing student and organization-related information.

The project was created as part of a Django development activity covering project setup, database modeling, Django Admin customization, test data generation, and project documentation.

## ✨ Features

### 🏫 College Management
- View registered colleges
- Search colleges by name
- Display college creation and update dates
- Filter colleges by creation date

### 🎓 Program Management
- View academic programs
- Display the college associated with each program
- Search programs by program name
- Search programs by college name
- Filter programs by college

### 🏢 Organization Management
- View student organizations
- Display organization name, college, and description
- Search organizations by name
- Search organizations by description
- Filter organizations by college

### 👨‍🎓 Student Management
- Store student information
- Associate students with academic programs
- View student details through Django Admin

### 🤝 Organization Membership
- Associate students with organizations
- Record organization membership dates
- Display the student's program and organization information

### 🔐 Django Admin
- Customized Django Admin interface
- Searchable records
- Filterable records
- Organized list displays for easier data management

## 🛠️ Technologies Used

- *Python*
- *Django*
- *SQLite*
- *Faker*
- *Git & GitHub*
- *HTML/CSS*
- *Django Admin*

## 📂 Project Structure

```text
PSUSphere/
│
├── projectsite/
│   ├── manage.py
│   ├── projectsite/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   └── studentorg/
│       ├── migrations/
│       ├── management/
│       │   └── commands/
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       └── ...
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Quick Setup & Run Guide
1. Setup & Activate Environment
git clone <paste repo url here>
cd PSUSphere
python -m venv psusenv

### Activate (Windows):
psusenv\Scripts\activate
### Activate (macOS/Linux):
source psusenv/bin/activate

2. Install Dependencies
pip install -r requirements.txt

3. Database Setup & Seed Data
cd projectsite
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser          # Create admin login
python manage.py create_initial_data      # Optional: populate fake data

4. Run & View Site
python manage.py runserver

 * App URL: http://127.0.0.1:8000/ #still empty
 * Admin URL: http://127.0.0.1:8000/admin/
