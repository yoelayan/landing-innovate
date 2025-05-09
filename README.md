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
4. Run the migrations:
   ```bash
   python manage.py migrate
   ```
5. Run the server:
   ```bash
   python manage.py runserver
   ```

## Deployment on Railway

### Environment Variables Required
Set the following environment variables in Railway:

- `SECRET_KEY`: Django secret key for security (required)
- `DEBUG`: Set to 'False' for production (default is 'False')
- `ALLOWED_HOSTS`: Comma-separated domains, e.g. '.railway.app,yourdomain.com' (default includes railway.app and localhost)
- `DATABASE_URL`: Automatically set by Railway if you provision a PostgreSQL database
- `PORT`: Automatically set by Railway

### Deploy Steps
1. Push your code to GitHub
2. Connect your GitHub repository to Railway
3. Railway will automatically build and deploy your application using the Dockerfile
4. Provision a PostgreSQL database if needed
5. Railway will automatically handle environment variables and deployment