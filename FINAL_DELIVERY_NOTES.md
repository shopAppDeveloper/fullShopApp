# Final delivery notes

This package is a consolidated source tree built from the actual uploaded frontend.zip and backend.zip, with the current application changes applied.

## Important

The code is not payment-complete because the payment provider was never selected. Production checkout is deliberately disabled until server-side payment verification is implemented.

## Verification

Static source verification performed:
- Frontend TS/TSX syntax parse: PASS
- Backend Python compileall: PASS

The analysis environment did not contain the installed frontend npm dependencies or Django/Oscar runtime packages, so a clean `npm run build`, `npm run lint`, `python manage.py test`, and live Django runtime test were not executed here.

## Development database

`backend/db.sqlite3` is included as a development snapshot so the current local catalogue can be preserved. Do not use that file as a production database.

Production should use PostgreSQL and a fresh database.

## Secrets

The uploaded `.env` / `.env.local` files are intentionally NOT included in the delivery. Create them from the provided `.env.example` files.
