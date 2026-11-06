# CURRENT PROJECT STATUS

This file is the current implementation summary. It supersedes older AI README assumptions when they conflict with actual source code.

## Delivered in the current codebase

### Frontend
- NextMerce UI retained as storefront base.
- Static NextMerce demo product source removed from live catalogue.
- Django/Oscar catalogue is used for product listing and product detail.
- Same-origin Next.js API proxy created at src/app/api/[...path]/route.ts.
- Same-origin Django media proxy created at src/app/media/[...path]/route.ts.
- Real product images load through the self-hosted backend.
- Product detail route uses /products/<slug>.
- Parent/child variant selection is supported.
- Server-backed Oscar basket is used instead of the template Redux cart.
- Django session auth/register/login/logout/current-user integration is wired.
- Saved addresses and customer orders are wired.
- Checkout UI is wired to backend order creation.
- Production checkout is intentionally blocked until payment provider verification is implemented.
- Homepage catalogue/category sections use backend data.
- Shop search/category/sort/pagination is backend-driven.
- Public store contact configuration uses NEXT_PUBLIC_* environment variables.

### Backend
- Django Oscar is the ecommerce authority.
- Product/category/country APIs exist.
- Oscar strategy determines price/availability.
- Basket API exists and uses Oscar Basket.
- Shipping endpoint currently exposes a zero-cost Standard Shipping method.
- Order creation uses Oscar OrderCreator and starts in Pending state.
- Customer address API exists.
- Customer order list/detail exists.
- CSRF/session authentication is used.
- Oscar country bootstrap command exists.
- PostgreSQL is the production database target.
- Whoosh/Haystack is local/self-hosted search.

## Explicit remaining production limitation

Payment provider integration is not implemented because the project owner has not selected a payment provider. Do NOT claim the store is payment-complete.

For production:
CHECKOUT_ALLOW_PENDING_ORDERS=False

A payment provider must be integrated server-side before production orders can be treated as paid.

## Verification performed on the consolidated source

- Frontend TypeScript/TSX syntax parsing: PASS.
- Backend Python compileall: PASS.

Not fully verified in this environment:
- npm install/build/lint (frontend dependencies are not installed in the analysis container).
- Django runtime tests (Django/Oscar are not installed in the analysis container).

The user previously confirmed during development:
- http://127.0.0.1:8000/api/products/ worked.
- http://127.0.0.1:3000/api/products/ worked.
- product image/media loading worked.

## Fresh-machine setup

Frontend:
1. npm install
2. create .env.local from .env.example
3. set DJANGO_INTERNAL_URL=http://127.0.0.1:8000
4. npm run dev

Backend:
1. create/activate venv
2. python -m pip install -r requirements.txt
3. python manage.py migrate
4. python manage.py bootstrap_store
5. python manage.py createsuperuser
6. python manage.py runserver

## Source of truth

The source files in frontend/ and backend/ are more authoritative than this document. This document exists only to help future AI assistants understand the implementation quickly.
