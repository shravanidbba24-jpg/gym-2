# Deploying Fitness Gym to Vercel

This full-stack application (Vite React + Python Serverless API) is fully configured for [Vercel](https://vercel.com).

---

## ⚡ Method 1: Deploy with Vercel CLI (Recommended)

Run the following commands in your project root:

```bash
# 1. Install the Vercel CLI globally
npm i -g vercel

# 2. Login to your Vercel account
vercel login

# 3. Deploy to production
vercel --prod
```

When prompted:
- **Set up and deploy?**: `y`
- **Which scope?**: Choose your personal account or team
- **Link to existing project?**: `N`
- **What's your project's name?**: `fitness-gym` (or press Enter)
- **In which directory is your code located?**: `./` (press Enter)
- **Want to modify these settings?**: `N` (Vercel will automatically read `vercel.json`)

---

## 🐙 Method 2: Deploy via GitHub / GitLab

1. Commit and push your code to GitHub:
   ```bash
   git add .
   git commit -m "Configure Vercel deployment"
   git push origin main
   ```
2. Open [vercel.com/new](https://vercel.com/new).
3. Select your repository and click **Import**.
4. The settings are pre-configured in `vercel.json`:
   - **Framework Preset**: `Vite`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Click **Deploy**. Vercel will build the frontend assets and deploy the Python Serverless Function (`api/index.py`) automatically.

---

## 🛠 Project Structure on Vercel

```
├── api/
│   ├── index.py           # Vercel serverless WSGI entrypoint
│   └── requirements.txt   # Serverless Python dependencies (Flask, Gunicorn)
├── dist/                  # Built static web assets (served by Vercel Edge CDN)
├── app.py                 # Full REST API implementation (CORS, resilience, fallback)
├── requirements.txt       # Root Python requirements
├── runtime.txt            # Specifies Python 3.11 runtime
├── vercel.json            # Routing & CORS rewrites
├── members.csv            # Member records storage
└── src/                   # React frontend application
```

---

## 🔍 How Routing Works on Vercel

1. **Client Routes (`/*`)**: Routed to `/index.html` (Vite SPA handles client-side routing).
2. **API Routes (`/api/*`, `/join`)**: Rewritten to `/api/index.py` (Flask serverless handler).
3. **Storage Resilience**: Automatically uses `/tmp/members.json` in serverless environments to avoid read-only filesystem errors.
