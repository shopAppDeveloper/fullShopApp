# Self-Hosted Shoes & Clothing Store

This project combines:
- NextMerce free Next.js storefront UI
- Django 5.2 + Django Oscar 4.2 backend
- Django REST Framework
- PostgreSQL in production / SQLite in local development
- local filesystem media
- local Haystack + Whoosh search
- Nginx + Gunicorn in production

No hosted CMS, hosted database, hosted auth, hosted search, Cloudinary, Sanity, Shopify, Vercel, Supabase, Firebase, or NextAuth is required. Payment processing is the only intentionally external service boundary.

## Current status

The storefront is connected to Oscar for products, categories, variants, images, basket, authentication, addresses, shipping and pending-order checkout.

Payment provider integration is intentionally not completed because a provider has not been selected. Production order creation is blocked until payment verification is configured.

Read PROJECT_STATUS_CURRENT.md first when an AI assistant continues this project.

## Development

### Backend

```bash
cd backend
python -m venv venv
```

Windows PowerShell:

```powershell
.\\venv\\Scripts\\Activate.ps1
```

Install:

```bash
python -m pip install -r requirements.txt
```

Database:

```bash
python manage.py migrate
python manage.py bootstrap_store
```

Create admin:

```bash
python manage.py createsuperuser
```

Run:

```bash
python manage.py runserver
```

Dashboard:
http://127.0.0.1:8000/dashboard/

### Frontend

```bash
cd frontend
npm install
```

Create `.env.local` from `.env.example` and set:

```env
DJANGO_INTERNAL_URL=http://127.0.0.1:8000
```

Optionally configure public storefront contact values using NEXT_PUBLIC_STORE_*.

Run:

```bash
npm run dev
```

Open:
http://127.0.0.1:3000

## Production

Use a fresh PostgreSQL database and a fresh production environment file. Do not deploy the development SQLite database or development secret.

Run Django under Gunicorn behind Nginx. Serve `/static/` and `/media/` from Nginx. Let Next.js expose same-origin `/api/*` routes that proxy to Django internally.

Set:

```env
DJANGO_DEBUG=False
DJANGO_SECURE_SSL_REDIRECT=True
DJANGO_HSTS_SECONDS=31536000
CHECKOUT_ALLOW_PENDING_ORDERS=False
```

Payment provider configuration must be added before enabling production checkout.
