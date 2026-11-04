# Fitness Gym — Production Deployment Guide
**Executive Clubs: Koregaon Park & Baner High Street, Pune, Maharashtra, India**

This project is built and optimized for seamless multi-platform deployment:
1. **Vercel** (Full-Stack Deployment: Vite React Frontend + Python Serverless API)
2. **Python Production WSGI** (Gunicorn / Render / Railway / Heroku / Fly.io)
3. **Docker & Container Deployment** (Local Docker Compose or Cloud Run)

---

## 1. Vercel Deployment (Full-Stack: React + Python Serverless API)

The repository includes pre-configured `vercel.json`, `.vercelignore`, and `api/index.py`.

### Option A: Via Vercel CLI (Fastest)
1. Install the Vercel CLI:
   ```bash
   npm i -g vercel
   ```
2. Log in and deploy from the project root:
   ```bash
   vercel
   ```
3. For production release:
   ```bash
   vercel --prod
   ```

### Option B: Via Vercel Git Integration (GitHub / GitLab / Bitbucket)
1. Push your repository to GitHub.
2. Go to [vercel.com](https://vercel.com) and click **"Add New Project"**.
3. Import your repository:
   - **Framework Preset**: `Vite`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. Click **Deploy**.

### How Vercel Routes Your App:
- Web UI visits (`/`, `/about`, `/records`, etc.) are served by Vite from the high-speed edge CDN (`dist/index.html`).
- REST API calls (`/api/members`, `/api/health`, `/join`, etc.) are routed automatically by `vercel.json` to the Python Serverless Function (`api/index.py` with Flask WSGI).
- Data persistence utilizes `/tmp/members.json` with in-memory caching to eliminate read-only filesystem errors.

---

## 2. Python Production Deployment (Gunicorn / Render / Railway)

### Requirements
Ensure dependencies are installed:
```bash
pip install -r requirements.txt
```

### Run Locally with Gunicorn
```bash
gunicorn app:app --bind 0.0.0.0:5000 --workers 2 --threads 4
```

### Run Locally with Zero Dependencies
If Flask is not installed, the built-in Python standard library server starts automatically:
```bash
python3 app.py
```

### Deploy to Render / Railway / Heroku
The included `Procfile` and `runtime.txt` configure the application automatically:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120`

---

## 3. Docker Container Deployment

### Build and Run with Docker
```bash
# Build the image
docker build -t fitness-gym-python .

# Run the container
docker run -d -p 5000:5000 --name fitness-gym fitness-gym-python
```

### Or using Docker Compose
```bash
docker compose up -d
```
Test health check:
```bash
curl http://localhost:5000/api/health
```

---

## 4. API Endpoints Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Web interface (or API health overview) |
| `GET` | `/api/health` | Service health status JSON |
| `GET` | `/api/members` | Retrieve all registered members |
| `POST` | `/api/members` or `/join` | Register new member |
| `DELETE` | `/api/members/<id>` | 1-Click delete member record |
| `DELETE` | `/api/members` | Clear all member records |
| `GET` | `/api/programs` | List training disciplines |
| `GET` | `/api/services` | List premium services & amenities |
| `GET` | `/api/reviews` | Member feedback & ratings |
| `GET` | `/api/export` | Download records as CSV file |
