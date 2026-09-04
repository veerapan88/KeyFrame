# KeyFrame

AI coordinator for self-managing landlords (leasing + maintenance). See
[`PRD_ KeyFrame _PropOps.md`](./PRD_%20KeyFrame%20_PropOps.md) for the product
spec and [`keyframe-v0-screen-ia.md`](./keyframe-v0-screen-ia.md) for the
screen inventory / information architecture.

This repo is the Phase 0 build: the landlord dashboard (PWA), the applicant
hosted-link pages, and the SMS thread reference views, implementing the
wireframes in [`design/KeyFrame Wireframes.dc.html`](./design/KeyFrame%20Wireframes.dc.html).

## Running it locally

You'll need Python 3.11+ installed.

```bash
python3 -m venv .venv
./.venv/bin/pip install -r backend/requirements.txt
cp .env.example .env
cd backend
../.venv/bin/python app.py
```

Then open http://127.0.0.1:5000 in a browser. The app runs on demo data out
of the box — you'll see a yellow banner at the top saying so — no Airtable
account needed to click around.

## Connecting real Airtable data

1. Create a new **blank base** at [airtable.com](https://airtable.com) (any
   name). Copy its base ID from the URL — it starts with `app...`.
2. Create a **Personal Access Token** at
   [airtable.com/create/tokens](https://airtable.com/create/tokens) scoped to
   that base, with these scopes: `data.records:read`, `data.records:write`,
   `schema.bases:write`.
3. Put both in `.env`:
   ```
   AIRTABLE_TOKEN=pat...
   AIRTABLE_BASE_ID=app...
   ```
4. Run the schema-creation script once:
   ```bash
   cd backend
   ../.venv/bin/python create_airtable_schema.py
   ```
   This creates all the tables (Property, Lead, Application, Screening Fee,
   etc.) and links between them. If Airtable gave your new base a default
   "Table 1", delete it by hand afterward — the script can't.
5. Restart the app. The yellow "demo data" banner disappears once
   `AIRTABLE_TOKEN`/`AIRTABLE_BASE_ID` are set, and every page starts reading
   from your real base instead of `backend/seed_data.py`. You'll need to add
   at least one Property record with criteria published before the applicant
   pages will do anything but show the hard-block state.

## Connecting Stripe (for the refund-execution buttons)

The refund *display* (status, countdown, the failure alert) works with no
Stripe key at all. The two buttons on the refund-failure screen that actually
move money need `STRIPE_SECRET_KEY` in `.env` — and only accept a **test
mode** key (starts with `sk_test_`) until this integration has had a real
review. Get one from your Stripe dashboard's test-mode API keys page.

## Running the tests

```bash
cd backend
../.venv/bin/python -m unittest discover tests -v
```

Covers `services/refund_engine.py` — the deadline math behind the refund
countdown (PRD §4 A5.4). Everything else in this build is UI wiring; this is
the one piece with a real statutory deadline attached.

## What's built vs. not

Built (from `design/KeyFrame Wireframes.dc.html`'s 18 screens): the pipeline
funnel, batch invite + refund-obligation interstitial, the criteria-matrix
comparison dashboard, the post-selection refund table, the refund-failure
alert, showings timeline, post-showing read cards (including the compliance-
guard "pending" state), the applicant fee-disclosure page and its hard-block
state, payment/portable-report/receipt, deposit checkout with the
Chicago/Cook jurisdiction block, and the three SMS thread reference views.

Not built (not in the wireframe file, so these are just nav stubs right now):
Properties (A2 listing prep, A3-S1 criteria builder UI — criteria are
currently only editable directly in Airtable), a real conversational Chat/AI
surface, and Settings (billing, Stripe connection UI).
