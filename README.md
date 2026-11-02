
# PSUSphere

A Django-based student organization management system for organizing and managing colleges, academic programs, student organizations, students, and organization memberships.

## 📌 About the Project

*PSUSphere* is a web application developed using *Django* and *SQLite*. It provides an administrative interface for managing student and organization-related information.

The project was created as part of a Django development activity covering project setup, database modeling, Django Admin customization, test data generation, project documentation, and Docker containerization.

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
- *Docker & Docker Compose*
- *Faker*
- *Git & GitHub*
- *HTML/CSS*
- *Django Admin*

---

## 🐳 Quick Setup & Run Guide (Using Docker)

### Prerequisites

* Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and ensure it is running.

### Developer Setup (Build from Source)

1. **Clone the repository:**
```bash
git clone <paste repo url here>
cd PSUSphere/projectsite

```


2. **Build and start the container:**
```bash
docker-compose up -d --build

```


3. **Verify container status:**
```bash
docker-compose ps

```


4. **Create Admin Superuser:**
```bash
docker-compose exec web python manage.py createsuperuser

```


5. **Access the application:**
* App URL: `http://localhost:8000/`
* Admin URL: `http://localhost:8000/admin/`



---

## 📦 Client Setup (Pull Pre-built Image from Docker Hub)

To run the application without building the source code:

1. Navigate to the `for_client` directory:
```bash
cd projectsite/for_client

```


2. Start the container:
```bash
docker-compose up -d

```



---

## 💻 Manual Setup & Local Execution (Without Docker)

1. **Setup & Activate Environment:**
```bash
git clone <paste repo url here>
cd PSUSphere
python -m venv psusenv

```


* **Activate (Windows):** `psusenv\Scripts\activate`
* **Activate (macOS/Linux):** `source psusenv/bin/activate`


2. **Install Dependencies:**
```bash
pip install -r projectsite/requirements.txt

```


3. **Database Setup & Seed Data:**
```bash
cd projectsite
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser          # Create admin login
python manage.py create_initial_data      # Optional: populate fake data

```


4. **Run Server:**
```bash
python manage.py runserver

```



---

## 🛠️ Useful Management Commands

* **View Live Container Logs:** `docker-compose logs -f web`
* **Stop Containers:** `docker-compose down`
* **Stop Containers & Clear Volumes:** `docker-compose down -v`

---

## 🌐 Live Deployment Links

* **App URL:** https://qtaqua.pythonanywhere.com/ (currently offline)
* **Admin URL:** https://qtaqua.pythonanywhere.com/admin (currently offline)

```

```