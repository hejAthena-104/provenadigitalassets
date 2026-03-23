# Dynamics Digital Asset

Investment platform with static frontend and Django backend.

## Project Structure

```
dynamicsdigitalasset/
├── frontend/              # Static landing pages (Netlify)
│   ├── index.html        # Homepage
│   ├── about-us.html
│   ├── crypto.html
│   ├── [27 more HTML pages]
│   ├── assets/           # Images and media
│   ├── css/              # Stylesheets
│   ├── js/               # JavaScript
│   ├── images/
│   ├── fonts/
│   ├── netlify.toml      # Netlify configuration
│   └── _redirects        # Redirect rules
│
└── backend/               # Django application (Railway/Render)
    ├── manage.py
    ├── config/           # Django settings
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    │   └── asgi.py
    ├── templates/        # HTML templates
    │   ├── auth/         # Login, register, forgot-password
    │   └── dashboard/    # Dashboard pages (16 files)
    ├── static/           # Static assets for dashboard
    │   └── themes/
    │       └── dashly/
    ├── media/            # User uploads
    ├── requirements.txt
    ├── Procfile          # For deployment
    ├── runtime.txt       # Python version
    └── .env.example      # Environment variables template
```

## Setup Instructions

### Frontend (Static Site)

The frontend is a collection of static HTML/CSS/JS files.

```bash
cd frontend
```

**Option 1: Open directly in browser**
```bash
# Simply open index.html in your browser
open index.html  # macOS
start index.html # Windows
```

**Option 2: Use a local server**
```bash
# Python
python -m http.server 8080

# Node.js
npx http-server -p 8080

# PHP
php -S localhost:8080
```

Then navigate to: `http://localhost:8080`

### Backend (Django)

**1. Create Virtual Environment**
```bash
cd backend
python -m venv venv

# Activate
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

**2. Install Dependencies**
```bash
pip install -r requirements.txt
```

**3. Set Up Environment Variables**
```bash
cp .env.example .env
# Edit .env with your settings
```

**4. Run Migrations** (when models are created)
```bash
python manage.py migrate
```

**5. Create Superuser** (when ready)
```bash
python manage.py createsuperuser
```

**6. Run Development Server**
```bash
python manage.py runserver
```

Backend will be available at: `http://localhost:8000`

## Deployment

### Frontend - Netlify

1. Connect your GitHub repository to Netlify
2. Set build settings:
   - **Base directory**: `frontend`
   - **Build command**: (leave empty for static site)
   - **Publish directory**: `frontend`
3. Update `netlify.toml` with your backend URL
4. Deploy!

### Backend - Railway

1. Connect your GitHub repository to Railway
2. Select the `backend` folder as root
3. Add a PostgreSQL database
4. Set environment variables:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=False
   ALLOWED_HOSTS=.railway.app
   DATABASE_URL=(auto-provided by Railway)
   FRONTEND_URL=https://your-frontend.netlify.app
   ```
5. Deploy!

### Backend - Render (Alternative)

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set:
   - **Root directory**: `backend`
   - **Build command**: `pip install -r requirements.txt`
   - **Start command**: `gunicorn config.wsgi`
4. Add PostgreSQL database
5. Set environment variables (same as Railway)
6. Deploy!

## Environment Variables

### Backend (.env)

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,.railway.app,.render.com
FRONTEND_URL=http://localhost:8080
DATABASE_URL=postgresql://... (for production)
```

See `backend/.env.example` for all available options.

## Current Status

✅ **Complete:**
- Project restructured into frontend/backend
- Django project initialized
- Templates organized (19 HTML files)
- Static assets moved
- Configuration files created
- Frontend links updated to point to backend

❌ **TODO (Implementation Phase):**
- Create Django apps (accounts, dashboard, transactions, investments)
- Define database models
- Implement authentication system
- Create views and URL patterns
- Build API endpoints (if using REST)
- Set up forms and validation
- Configure admin panel
- Add payment integration
- Implement email notifications
- Write tests
- Actual deployment

## Key Files

### Frontend
- `frontend/index.html` - Homepage
- `frontend/netlify.toml` - Netlify configuration
- `frontend/_redirects` - Redirect rules

### Backend
- `backend/config/settings.py` - Django settings
- `backend/config/urls.py` - URL routing
- `backend/manage.py` - Django management script
- `backend/requirements.txt` - Python dependencies
- `backend/Procfile` - Deployment configuration

## Links

Authentication and dashboard links in frontend now point to:
- Register: `http://localhost:8000/auth/register`
- Login: `http://localhost:8000/auth/login`
- Dashboard: `http://localhost:8000/dashboard/`

**Note:** Update these URLs in production by modifying `netlify.toml` and `_redirects`.

## Tech Stack

**Frontend:**
- HTML5, CSS3, JavaScript
- Bootstrap
- jQuery
- TradingView widgets
- Coinlib widgets

**Backend:**
- Django 4.2.7
- Python 3.11
- Gunicorn (production server)
- WhiteNoise (static files)
- PostgreSQL (production)
- SQLite (development)

## Next Steps

1. Install Django dependencies: `cd backend && pip install -r requirements.txt`
2. Create Django apps for your features
3. Define database models
4. Implement authentication
5. Build out views and templates
6. Test locally
7. Deploy to Netlify + Railway/Render

## Development

- Frontend runs on: `http://localhost:8080`
- Backend runs on: `http://localhost:8000`
- Admin panel: `http://localhost:8000/admin/`

## Support

For Django documentation: https://docs.djangoproject.com/
For Netlify docs: https://docs.netlify.com/
For Railway docs: https://docs.railway.app/

---

**Note:** This project is currently in the setup phase. The structure is ready, but implementation details (models, views, authentication, etc.) need to be built out.
