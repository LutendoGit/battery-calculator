# Battery Calculator — Flask Web App

This repository contains a web front-end for the original `battery_calculator.py` script. The UI is built with Flask and the computation logic is in `calculator.py`.

Quick start (Windows PowerShell):

1. Create and activate a virtual environment (optional but recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app:

```powershell
# Battery Calculator — Flask Web App

This repository contains a Flask web wrapper for your battery design calculator. It includes server-side PDF export (via `reportlab`) and an improved UI.

## Quick local demo (Windows PowerShell)

1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app locally:

```powershell
python .\app.py
```

By default the app listens on `http://127.0.0.1:5000`.

### Temporary public link (ngrok)
If you want a temporary public URL for quick sharing or webhook testing, use `ngrok`:

```powershell
ngrok http 5000
```

Copy the `https://...` forwarding URL shown by `ngrok` and share it. Note that free ngrok URLs are temporary.

## Deploying to a cloud host (Render example)
This repo includes a `Procfile` and `gunicorn` in `requirements.txt` so it can be deployed to Render, Railway, Fly.io, or Heroku.

Steps to deploy to Render:

1. Push the repo to GitHub (create a repo and push your local code):

```powershell
git init
git add .
git commit -m "Initial Flask battery calculator app"
# Create a GitHub repo via the web UI or `gh` CLI, then push:
git remote add origin https://github.com/<your-username>/<repo>.git
git push -u origin main
```

2. In Render:
	- Sign in and create a new **Web Service**.
	- Connect your GitHub repo and select the branch to deploy.
	- Build command: leave blank or use `pip install -r requirements.txt`.
	- Start command: `gunicorn app:app`.
	- Add environment variables in Render dashboard (see below).

3. Add environment variables (important):
	- `SECRET_KEY` — set to a secure random string (do NOT use `'dev'` in production).

Render will provide a stable public URL (e.g., `https://your-app.onrender.com`).

### Other hosts
- **Heroku**: similar flow using `Procfile` and `gunicorn`.
- **Railway**: connect GitHub and set `Start Command` to `gunicorn app:app`.
- **Fly.io**: may require a Dockerfile or buildpack.
- **PythonAnywhere**: configure a WSGI app (different flow than `gunicorn`).

## Production considerations

- Secrets: set `SECRET_KEY` as an environment variable on your host.
- Static files / large assets: consider a CDN or object storage.
- Logging & monitoring: configure the host's log viewer or add Sentry.
- PDF generation: `reportlab` is included; ensure your host supports installing it.

## Troubleshooting

- If PDF generation fails on the host, confirm `reportlab` installed and check build logs for wheel compatibility.
- If the UI looks wrong, clear the browser cache or check the browser console for missing assets.

## Files of interest

- `app.py` — Flask app and routes (includes `/export-pdf`).
- `calculator.py` — calculation logic returning dictionaries with `summary_text`.
- `templates/` — HTML templates (`index.html`, `result.html`).
- `requirements.txt` — dependencies, includes `gunicorn` and `reportlab`.
- `Procfile` — `web: gunicorn app:app` for many hosts.
- `runtime.txt` — (optional) Python runtime version pin.

If you want, I can:
- Push this repo to GitHub for you (I can show commands or run them if you allow).
- Walk through Render or Railway deployment step-by-step and configure environment variables.
- Create a GitHub Actions workflow for CI / automated deploys.
