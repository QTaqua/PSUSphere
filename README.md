# PSUSphere

PSUSphere is a Django student-organization registry for managing colleges, academic programs, organizations, students, and organization memberships. It includes a responsive dashboard, searchable CRUD pages, Django Admin, and username/email plus Google or GitHub authentication through django-allauth.

## Features

- Login-protected dashboard with student, organization, program, and current-year membership counts
- Read access for signed-in users and permission-controlled create, update, and delete flows for all five registry models
- Search on every list page
- Organization ordering by college/name, program sorting by program/college, and member sorting by student/date joined
- Paginated, responsive templates with keyboard-visible focus states
- Username or email login, registration, password reset, Google login, and GitHub login
- Customized Django Admin and a fresh-database-safe Faker seed command
- PythonAnywhere-ready allowed-host, static-file, and WSGI configuration inputs

## Authors

- QTaqua and the PSUSphere course project contributors

## Local setup

```powershell
git clone <repository-url>
cd PSUSphere
python -m venv psusenv
psusenv\Scripts\activate
pip install -r requirements.txt
cd projectsite
python manage.py migrate
python manage.py createsuperuser
python manage.py create_initial_data
python manage.py runserver
```

Open `http://localhost:8000/`. Anonymous visitors are redirected to the account login page; Django Admin is at `http://localhost:8000/admin/`.

## Social login setup

1. Run migrations, then sign in to Django Admin.
2. Under **Sites**, set site ID `1` to `localhost:8000` for local work. Set `DJANGO_SITE_ID` if your selected Site uses another ID.
3. Create Google and/or GitHub OAuth applications with these local callback URLs:
   - `http://localhost:8000/accounts/google/login/callback/`
   - `http://localhost:8000/accounts/github/login/callback/`
4. In **Social applications**, add each provider's client ID and secret and attach the current Site.

OAuth credentials belong in Django Admin or environment-backed deployment configuration; never commit them.

## Environment settings

| Variable | Default | Purpose |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | Local development-only fallback | Set a strong secret in production |
| `DJANGO_DEBUG` | `True` | Set to `False` in production |
| `DJANGO_ALLOWED_HOSTS` | `127.0.0.1,localhost,qtaqua.pythonanywhere.com` | Comma-separated accepted hosts |
| `DJANGO_SITE_ID` | `1` | Site record used by django-allauth |
| `DJANGO_EMAIL_BACKEND` | SMTP backend in production | Use a non-console Django email backend when `DJANGO_DEBUG=False` |
| `DJANGO_EMAIL_HOST` | None | Required SMTP server when the production SMTP backend is used |
| `DJANGO_EMAIL_PORT` | `587` | Production SMTP port |
| `DJANGO_EMAIL_HOST_USER` | Empty | Production SMTP username |
| `DJANGO_EMAIL_HOST_PASSWORD` | Empty | Production SMTP password; keep it outside Git |
| `DJANGO_EMAIL_USE_TLS` | `True` | Enable TLS for production SMTP |
| `DJANGO_DEFAULT_FROM_EMAIL` | None | Required sender address for production SMTP |

## PythonAnywhere deployment

1. Clone the repository, create/activate a virtual environment, and run `pip install -r requirements.txt`.
2. Set the web app source path to the directory containing `manage.py` (`.../PSUSphere/projectsite`).
3. Set `DJANGO_DEBUG=False`, `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, the deployed `DJANGO_SITE_ID`, and the production email variables in the PythonAnywhere environment/WSGI configuration. Production startup fails if the secret or SMTP host/from address is missing.
4. Configure the WSGI module with `DJANGO_SETTINGS_MODULE=projectsite.settings`, then run:

   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

5. Add the deployed domain as a Django Site and attach it to each Social Application. Add the deployed OAuth callbacks, for example `https://qtaqua.pythonanywhere.com/accounts/google/login/callback/`.
6. Reload the PythonAnywhere web app.

## Verification

From the directory containing `manage.py`:

```powershell
python manage.py check
python manage.py test
python manage.py collectstatic --noinput
```
