# Fitness Gym - High-Performance Training Club (Pune, India)
## Vercel Deployment & Full-Stack Architecture

### 🚀 Deploying to Vercel in 1 Minute

This repository is pre-configured with `vercel.json`, `api/index.py`, and `requirements.txt` for immediate deployment on [Vercel](https://vercel.com).

#### Option 1: Deploy with Vercel CLI
```bash
# 1. Install Vercel CLI (if not already installed)
npm i -g vercel

# 2. Deploy preview from project root
vercel

# 3. Deploy to production
vercel --prod
```

#### Option 2: Deploy via GitHub / GitLab on Vercel Dashboard
1. Push this project to your GitHub repository.
2. In Vercel, click **Add New...** -> **Project**.
3. Select your repository.
4. Framework Preset will be automatically detected as **Vite**:
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Click **Deploy**. Both the Vite frontend and the Python Serverless Function (`/api/index.py`) will build and deploy automatically!

---

### 📁 Vercel Project Routing Architecture
- Frontend: `dist/index.html` (Vite SPA) routes all user pages (`/`, `/*`)
- Serverless API: `/api/(.*)` & `/join` route directly to `api/index.py` (Flask WSGI)
- Storage Resilience: Falls back to `/tmp/members.json` with memory caching in serverless environments to prevent read-only filesystem errors.
