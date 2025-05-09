# landing-innova7e

This is the repository for the landing page of Innova7e.

## Structure
```
landing-innova7e
├─ app
│  ├─ apps
│  │  └─ pages
│  │     ├─ __init__.py
│  │     ├─ admin.py
│  │     ├─ apps.py
│  │     ├─ migrations
│  │     │  └─ __init__.py
│  │     ├─ models.py
│  │     ├─ templates
│  │     │  ├─ page_home.html
│  │     │  └─ partials
│  │     ├─ tests.py
│  │     └─ views.py
│  ├─ config
│  │  ├─ __init__.py
│  │  ├─ __pycache__
│  │  │  ├─ __init__.cpython-312.pyc
│  │  │  ├─ settings.cpython-312.pyc
│  │  │  └─ urls.cpython-312.pyc
│  │  ├─ asgi.py
│  │  ├─ settings.py
│  │  ├─ urls.py
│  │  └─ wsgi.py
│  ├─ manage.py
│  ├─ templates
│  │  ├─ components
│  │  ├─ layout
│  │  │  ├─ layout_blank.html
│  │  │  ├─ layout_front.html
│  │  │  ├─ master.html
│  │  │  └─ partials
│  │  │     ├─ footer
│  │  │     ├─ messages
│  │  │     ├─ navbar
│  │  │     ├─ scripts.html
│  │  │     └─ styles.html
│  │  ├─ misc
│  │  └─ partials
│  │     └─ logo.html
│  └─ web_project
│     ├─ __init__.py
│     ├─ template_helpers
│     │  └─ __init__.py
│     └─ template_tags
│        └─ __init__.py
├─ backups
├─ readme.MD
└─ requirements.txt

```
## Run Project in local
1. Create a virtual environment:
   ```bash
   virtualenv .venv
   ```
2. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
3. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a .env file in the root of the project:
   ```bash
   touch .env
   ```
   Add the following content to the .env file:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```
5. Run the migrations:
   ```bash
   python app/manage.py migrate
   ```
6. Run the server:
   ```bash
   python app/manage.py runserver
   ```

## Deployment on Railway

### Environment Variables Required
Set the following environment variables in Railway:

- `SECRET_KEY`: Django secret key for security (required)
- `DEBUG`: Set to 'False' for production
- `ALLOWED_HOSTS`: Comma-separated domains without spaces, e.g. 'localhost,127.0.0.1,.railway.app,yourdomain.com'
- `DATABASE_URL`: Automatically set by Railway if you provision a PostgreSQL database
- `PORT`: Automatically set by Railway

### Superuser Credentials
You can configure a default superuser to be created automatically on startup:

- `DJANGO_SUPERUSER_USERNAME`: The username for the superuser (default: 'admin')
- `DJANGO_SUPERUSER_EMAIL`: The email for the superuser (default: 'admin@example.com')
- `DJANGO_SUPERUSER_PASSWORD`: The password for the superuser (default: 'admin_password')

**IMPORTANT**: Be sure to change these default values in production!

### Deploy Steps
1. Push your code to GitHub
2. Connect your GitHub repository to Railway
3. Set up the required environment variables in Railway
4. Railway will automatically build and deploy your application using the Dockerfile
5. Provision a PostgreSQL database if needed

### Notes
- We're using django-environ for environment variable management
- The application is configured to work with either SQLite or PostgreSQL automatically
- Static files are collected during the Docker build process