# Fitness Gym India (भारतीय फिटनेस जिम) - Full Python Project

A complete fitness gym web application and Python backend localized for India (Mumbai, New Delhi, Bengaluru, Pune). Features Olympic strength training, authentic Indian high-protein diet plans (Vegetarian & Non-Veg), certified Indian coaches, interactive BMI tool, class schedule, and persistent member database registry.

---

## 🇮🇳 India Localization Highlights

1. **Brand & Centers**:
   - **Fitness Gym India** (`FG India 🇮🇳`)
   - 4 Major City Hubs: **Mumbai** (Bandra West), **New Delhi** (Connaught Place), **Bengaluru** (Indiranagar), and **Pune** (Koregaon Park).

2. **Programs & Coaches**:
   - **Weight Training (स्ट्रेंथ ट्रेनिंग)** with Gold Medalist Coach Rahul Sharma.
   - **Cardio & Stamina (कार्डियो और स्टेमिना)** with Marathon Coach Priya Nair.
   - **Traditional Yoga (योग और प्राणायाम)** with Rishikesh-certified Yogacharya Vikram Singh.

3. **Desi High-Protein Nutrition Plans**:
   - **Shakahari (शाकाहारी) High-Protein**: 2,350 kcal / 145g protein featuring Paneer Bhurji, Sattu drink, Moong Dal Khichdi, Soya Chunks, and Sprouted Chana.
   - **Power & Lean Muscle Plan**: 2,550 kcal / 175g protein featuring boiled eggs, tandoori chicken, dal tadka, and whole grains.

4. **Persistent Members Registry**:
   - Pre-seeded with Indian members: Rahul Sharma (Mumbai), Sneha Patel (Bengaluru), Amit Kumar (Pune), and Kavita Verma (New Delhi).
   - Form pre-filled with placeholder `Kavita` / `kavita@example.com` and `+91` phone numbers.
   - Saves registrations to `members.json` and persistent browser storage.
   - Search, filter by city or program, digital pass generator, and CSV export.

---

## 🐍 Python Full Project Architecture

The project includes a full Python 3 backend in `app.py`:

- **Dual-Mode Engine**: Supports **Flask** (production WSGI) and Python's built-in **`http.server`** standard library (zero-dependency fallback).
- **REST API Endpoints**:
  - `GET /` — Serves the full Indian gym web application (`templates/index.html`)
  - `GET /api/members` — Returns all registered member records from `members.json`
  - `POST /join` — Registers new member, assigns Member ID (`FIT-IN-XXXX`), and persists to `members.json`
  - `GET /api/programs` — Returns Indian gym programs and certified coaches
  - `GET /api/diet-plans` — Returns Vegetarian and Non-Veg high-protein meal charts
  - `GET /api/services` — Returns gym amenities and equipment specifications

### How to Run with Python

```bash
# Option 1: Run with Python standard library (zero extra installs required!)
python3 app.py

# Option 2: Run with Flask
pip install -r requirements.txt
python3 app.py
```

Server runs on `http://localhost:5000` (or the port specified by `$PORT`).
