# Production deployment outline

Target:

Internet -> Nginx -> Next.js
                  \-> /media + /static directly
Next.js server routes -> Django/Gunicorn -> PostgreSQL

Recommended host directories:
/srv/my-shop/frontend
/srv/my-shop/backend

Production environment:
- real DJANGO_SECRET_KEY
- DJANGO_DEBUG=False
- real DJANGO_ALLOWED_HOSTS
- real DJANGO_CSRF_TRUSTED_ORIGINS=https://your-domain
- PostgreSQL credentials
- DJANGO_INTERNAL_URL=http://127.0.0.1:8000
- CHECKOUT_ALLOW_PENDING_ORDERS=False until payment verification is integrated

High-level commands:

Backend:
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py bootstrap_store
python manage.py collectstatic --noinput
gunicorn config.wsgi:application --bind 127.0.0.1:8000

Frontend:
npm install
npm run build
npm run start -- --hostname 127.0.0.1 --port 3000

See nginx.conf.example and the systemd examples in this directory.
