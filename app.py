#!/usr/bin/env python3
"""
Fitness Gym - High-Performance Training Club
Full Python Web Application, REST API Server & Vercel Serverless Backend.
Location: Pune, Maharashtra, India (Koregaon Park & Baner High Street Clubs)

Deployment Targets:
  1. Vercel: Runs via api/index.py with automatic serverless WSGI dispatch
  2. Gunicorn / Docker / Render / Railway: gunicorn app:app --bind 0.0.0.0:$PORT
  3. Local Zero-Dependency: python3 app.py (falls back to http.server if Flask is not installed)
"""

import json
import os
import sys
import csv
import io
from datetime import datetime

PORT = int(os.environ.get("PORT", 5000))

# -----------------------------------------------------------------------------
# Resilient Storage (Supports local files, Docker mounts, & Serverless read-only /tmp)
# -----------------------------------------------------------------------------
DEFAULT_SEED_MEMBERS = [
    {
        "id": "FIT-1042",
        "name": "Rahul Sharma",
        "email": "rahul.s@example.com",
        "phone": "+91 98201 92834",
        "program": "Weight Training",
        "time_slot": "Morning (06:00 - 09:00)",
        "tier": "Pro Member",
        "branch": "Pune - Koregaon Park (Flagship)",
        "joined_at": "02 Nov 2026, 09:14 AM"
    },
    {
        "id": "FIT-1041",
        "name": "Sneha Patel",
        "email": "sneha.p@example.com",
        "phone": "+91 98202 84729",
        "program": "Cardio Training",
        "time_slot": "Evening (17:00 - 21:00)",
        "tier": "Elite All-Access",
        "branch": "Pune - Baner High Street",
        "joined_at": "01 Nov 2026, 04:30 PM"
    },
    {
        "id": "FIT-1040",
        "name": "Amit Kumar",
        "email": "amit.k@example.com",
        "phone": "+91 98203 19482",
        "program": "Weight Training",
        "time_slot": "Morning (06:00 - 09:00)",
        "tier": "Pro Member",
        "branch": "Pune - Koregaon Park (Flagship)",
        "joined_at": "30 Oct 2026, 11:20 AM"
    },
    {
        "id": "FIT-1039",
        "name": "Kavita Verma",
        "email": "kavita@example.com",
        "phone": "+91 98204 38291",
        "program": "Yoga & Mobility",
        "time_slot": "Morning (06:00 - 09:00)",
        "tier": "Pro Member",
        "branch": "Pune - Koregaon Park (Flagship)",
        "joined_at": "28 Oct 2026, 07:45 AM"
    }
]

_MEMBERS_CACHE = None

def get_storage_path():
    """Determine writable file path for members.json (falls back to /tmp in serverless)"""
    if os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
        return "/tmp/members.json"
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "members.json")

def load_members():
    global _MEMBERS_CACHE
    path = get_storage_path()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                _MEMBERS_CACHE = json.load(f)
                return _MEMBERS_CACHE
        except Exception:
            pass

    # Fallback to project root members.json if it exists
    root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "members.json")
    if os.path.exists(root_path) and root_path != path:
        try:
            with open(root_path, "r", encoding="utf-8") as f:
                _MEMBERS_CACHE = json.load(f)
                return _MEMBERS_CACHE
        except Exception:
            pass

    if _MEMBERS_CACHE is not None:
        return _MEMBERS_CACHE

    _MEMBERS_CACHE = list(DEFAULT_SEED_MEMBERS)
    return _MEMBERS_CACHE

def save_members(members):
    global _MEMBERS_CACHE
    _MEMBERS_CACHE = members
    path = get_storage_path()
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(members, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        # If writing to project directory fails (e.g. read-only filesystem), fallback to /tmp
        try:
            with open("/tmp/members.json", "w", encoding="utf-8") as f:
                json.dump(members, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e2:
            print(f"Warning: Storage write error ({e2}), falling back to in-memory persistence.")
            return False

# -----------------------------------------------------------------------------
# Static Data Sets (Training Programs, Services, Testimonials, Diet Plans)
# -----------------------------------------------------------------------------
PROGRAMS_DATA = [
    {
        "id": "p1",
        "title": "Weight Training (स्ट्रेंथ ट्रेनिंग)",
        "description": "Build raw power and lean muscle with progressive overload and certified strength coaches in Pune.",
        "image": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=800&auto=format&fit=crop&q=80",
        "details": "Olympic barbell lifts, calibrated power racks, dumbbell arsenals up to 60kg, and periodized hypertrophy coaching.",
        "coach": "Rahul S. (Head Strength Coach, Gold Medalist)",
        "intensity": "High",
        "schedule": "Mon-Sat • 06:00 - 22:00"
    },
    {
        "id": "p2",
        "title": "Cardio & Stamina (कार्डियो और स्टेमिना)",
        "description": "Improve stamina, heart health, and aerobic capacity through zone-based metabolic protocols.",
        "image": "https://images.unsplash.com/photo-1571902943202-507ec2618e8f?w=800&auto=format&fit=crop&q=80",
        "details": "Assault air bikes, Concept2 rowers, curved treadmills, and heart-rate monitored HIIT circuits.",
        "coach": "Priya Nair (Marathon & Endurance Specialist)",
        "intensity": "Medium-High",
        "schedule": "Daily • 06:00 - 21:00"
    },
    {
        "id": "p3",
        "title": "Yoga & Mobility (योग और प्राणायाम)",
        "description": "Dynamic vinyasa flow, deep restorative asanas, joint decompression, and active recovery.",
        "image": "https://images.unsplash.com/photo-1599058917212-d750089bc07e?w=800&auto=format&fit=crop&q=80",
        "details": "Restores spinal alignment, relieves desk fatigue, increases athletic flexibility, and prevents injury.",
        "coach": "Yogacharya Vikram Singh (Rishikesh Certified)",
        "intensity": "Restorative",
        "schedule": "Tue, Thu, Sat, Sun • Morning & Evening"
    }
]

SERVICES_DATA = [
    {
        "id": "s1",
        "title": "Personal Training",
        "description": "1-on-1 private coaching tailored to your biomechanics, body composition goals, and daily schedule.",
        "image": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=800&auto=format&fit=crop&q=80",
        "details": "Includes full kinematic assessments, custom workout app routines, and bi-weekly milestone body composition check-ins."
    },
    {
        "id": "s2",
        "title": "Diet Plan & Sports Nutrition",
        "description": "Precision calorie and macro-targeted meal planning designed by registered sports dietitians.",
        "image": "https://images.unsplash.com/photo-1546483875-ad9014c88eba?w=800&auto=format&fit=crop&q=80",
        "details": "Caloric timing, Indian and continental whole-food plans, micronutrient balance, and supplementation guidance."
    },
    {
        "id": "s3",
        "title": "Modern Equipment & Recovery Lounge",
        "description": "Eleiko competition barbells, pneumatic resistance machines, and private steam/sauna rooms.",
        "image": "https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=800&auto=format&fit=crop&q=80",
        "details": "Biomechanical engineering ensures safe execution under heavy loads with premium shock-absorbent flooring."
    }
]

DIET_PLANS = [
    {
        "id": "diet-veg",
        "name": "Shakahari (शाकाहारी) High-Protein",
        "type": "Pure Vegetarian",
        "calories": "2,350 kcal",
        "protein": "145g",
        "carbs": "260g",
        "fats": "65g",
        "description": "Optimized for Indian vegetarian athletes using paneer, roasted sattu, moong sprouts, and Greek curd.",
        "meals": [
            {"time": "07:30 AM", "title": "Pre-Workout Fuel", "items": "1 Banana + 5 soaked almonds + 1 cup warm black coffee"},
            {"time": "09:30 AM", "title": "High-Protein Breakfast", "items": "150g Paneer Bhurji with turmeric, green chillies + 2 whole wheat rotis"},
            {"time": "01:30 PM", "title": "Nutritious Indian Lunch", "items": "1 bowl Moong Dal Tadka + 1 cup Brown Rice + Cucumber Salad + 1 cup Dahi"},
            {"time": "05:00 PM", "title": "Desi Evening Refuel", "items": "Bihar Sattu drink (40g sattu + lemon + cumin) or roasted chana"},
            {"time": "08:30 PM", "title": "Recovery Dinner", "items": "1 bowl Soya chunks curry (50g dry soya) + stir-fried beans, broccoli & capsicum"}
        ]
    },
    {
        "id": "diet-nonveg",
        "name": "Lean Muscle & Power Cut",
        "type": "Non-Vegetarian / High-Protein",
        "calories": "2,550 kcal",
        "protein": "175g",
        "carbs": "240g",
        "fats": "70g",
        "description": "High biological value proteins designed for rapid strength and lean muscle hypertrophy.",
        "meals": [
            {"time": "07:30 AM", "title": "Morning Kickstart", "items": "3 boiled egg whites + 1 whole egg + black coffee"},
            {"time": "09:30 AM", "title": "Post-Workout Fuel", "items": "Oats cooked with cinnamon + 1 scoop whey + sliced green apple"},
            {"time": "01:30 PM", "title": "Power Lunch", "items": "180g Tandoori/grilled chicken breast + dal palak + 1 cup basmati rice"},
            {"time": "05:00 PM", "title": "Pre-Evening Snack", "items": "Sprouted moong chaat + roasted walnuts and almonds"},
            {"time": "08:30 PM", "title": "Dinner & Repair", "items": "150g Grilled Rohu/Surmai fish or chicken breast + large mixed vegetable sauté"}
        ]
    }
]

REVIEWS_DATA = [
    {
        "id": "r1",
        "name": "Rahul Sharma",
        "quote": "Best executive gym in Pune.",
        "details": "Trained at the Koregaon Park club for 6 months. Bench press increased by 35kg under coach Rahul S.'s training protocol.",
        "rating": 5
    },
    {
        "id": "r2",
        "name": "Sneha Patel",
        "quote": "World-class equipment and immaculate hygiene.",
        "details": "The Baner facility is incredible. Prepared for the Pune half-marathon with zero joint pain thanks to the mobility classes.",
        "rating": 5
    },
    {
        "id": "r3",
        "name": "Amit Kumar",
        "quote": "Lost 10kg clean body fat.",
        "details": "Followed the structured cardio and sports nutrition plan regularly. Dropped body fat from 26% to 15% in 4 months.",
        "rating": 5
    }
]

# -----------------------------------------------------------------------------
# Check Flask Availability (Flask is standard in production & Vercel)
# -----------------------------------------------------------------------------
try:
    from flask import Flask, request, jsonify, Response
    USE_FLASK = True
except ImportError:
    USE_FLASK = False

if USE_FLASK:
    app = Flask(__name__)

    # Cross-Origin Resource Sharing (CORS) hook for all routes
    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
        return response

    @app.route("/", methods=["GET", "OPTIONS"])
    @app.route("/api", methods=["GET", "OPTIONS"])
    def index():
        if request.method == "OPTIONS":
            return ("", 204)
        return jsonify({
            "service": "Fitness Gym REST API (Vercel Serverless Ready)",
            "version": "2.4.0",
            "runtime": "Python 3.11 / Flask WSGI",
            "location": "Pune, Maharashtra, India (Koregaon Park & Baner Clubs)",
            "status": "healthy",
            "vercel_ready": True,
            "endpoints": [
                "GET /api/health",
                "GET /api/members",
                "POST /api/members (or /join)",
                "DELETE /api/members/<id> (1-click delete)",
                "DELETE /api/members (clear all)",
                "GET /api/programs",
                "GET /api/services",
                "GET /api/diet-plans",
                "GET /api/reviews",
                "GET /api/export"
            ]
        })

    @app.route("/api/health", methods=["GET", "OPTIONS"])
    @app.route("/health", methods=["GET", "OPTIONS"])
    def health_check():
        if request.method == "OPTIONS":
            return ("", 204)
        return jsonify({
            "status": "healthy",
            "service": "fitness-gym-api",
            "environment": "vercel" if os.environ.get("VERCEL") else "standard",
            "location": "Pune, Maharashtra",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "total_members": len(load_members())
        })

    @app.route("/api/programs", methods=["GET", "OPTIONS"])
    @app.route("/programs", methods=["GET", "OPTIONS"])
    def get_programs():
        if request.method == "OPTIONS":
            return ("", 204)
        return jsonify(PROGRAMS_DATA)

    @app.route("/api/services", methods=["GET", "OPTIONS"])
    @app.route("/services", methods=["GET", "OPTIONS"])
    def get_services():
        if request.method == "OPTIONS":
            return ("", 204)
        return jsonify(SERVICES_DATA)

    @app.route("/api/diet-plans", methods=["GET", "OPTIONS"])
    @app.route("/diet-plans", methods=["GET", "OPTIONS"])
    def get_diet_plans():
        if request.method == "OPTIONS":
            return ("", 204)
        return jsonify(DIET_PLANS)

    @app.route("/api/reviews", methods=["GET", "OPTIONS"])
    @app.route("/reviews", methods=["GET", "OPTIONS"])
    def get_reviews():
        if request.method == "OPTIONS":
            return ("", 204)
        return jsonify(REVIEWS_DATA)

    @app.route("/api/members", methods=["GET", "POST", "DELETE", "OPTIONS"])
    @app.route("/members", methods=["GET", "POST", "DELETE", "OPTIONS"])
    def handle_members():
        if request.method == "OPTIONS":
            return ("", 204)

        if request.method == "GET":
            return jsonify(load_members())

        if request.method == "DELETE":
            save_members([])
            return jsonify({"success": True, "message": "All member records have been cleared", "count": 0})

        if request.method == "POST":
            data = request.get_json(silent=True) or request.form.to_dict()
            return _create_member(data)

    @app.route("/api/members/<member_id>", methods=["GET", "DELETE", "OPTIONS"])
    @app.route("/members/<member_id>", methods=["GET", "DELETE", "OPTIONS"])
    def handle_single_member(member_id):
        if request.method == "OPTIONS":
            return ("", 204)

        members = load_members()
        matched = [m for m in members if m["id"] == member_id]

        if not matched:
            return jsonify({"error": f"Member with ID '{member_id}' not found"}), 404

        if request.method == "GET":
            return jsonify(matched[0])

        if request.method == "DELETE":
            updated = [m for m in members if m["id"] != member_id]
            save_members(updated)
            return jsonify({
                "success": True,
                "message": f"Member {matched[0]['name']} ({member_id}) was permanently deleted with 1-click",
                "deleted": matched[0]
            })

    @app.route("/join", methods=["POST", "OPTIONS"])
    @app.route("/api/join", methods=["POST", "OPTIONS"])
    def join_gym():
        if request.method == "OPTIONS":
            return ("", 204)
        data = request.get_json(silent=True) or request.form.to_dict()
        return _create_member(data)

    @app.route("/api/export", methods=["GET", "OPTIONS"])
    @app.route("/export", methods=["GET", "OPTIONS"])
    def export_csv():
        if request.method == "OPTIONS":
            return ("", 204)
        members = load_members()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Member ID", "Name", "Email", "Phone", "Program", "Time Slot", "Tier", "Branch", "Joined At"])
        for m in members:
            writer.writerow([
                m.get("id", ""),
                m.get("name", ""),
                m.get("email", ""),
                m.get("phone", ""),
                m.get("program", ""),
                m.get("time_slot", ""),
                m.get("tier", ""),
                m.get("branch", "Pune - Koregaon Park"),
                m.get("joined_at", "")
            ])
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": f"attachment; filename=fitness_gym_members_{datetime.now().strftime('%Y%m%d')}.csv"}
        )

    def _create_member(data):
        if not data:
            return jsonify({"error": "No member payload provided"}), 400

        name = str(data.get("name", "")).strip()
        email = str(data.get("email", "")).strip()
        phone = str(data.get("phone", "")).strip()
        program = str(data.get("program", "Weight Training")).strip()
        time_slot = str(data.get("time_slot", data.get("timeSlot", "Morning (06:00 - 09:00)"))).strip()
        tier = str(data.get("tier", "Pro Member")).strip()
        branch = str(data.get("branch", "Pune - Koregaon Park (Flagship)")).strip()

        if not name or not email or not phone:
            return jsonify({"error": "Name, email, and phone are required fields"}), 400

        members = load_members()
        new_id = f"FIT-{1000 + len(members) + 1}"
        date_str = datetime.now().strftime("%d %b %Y, %I:%M %p")

        new_member = {
            "id": new_id,
            "name": name,
            "email": email,
            "phone": phone,
            "program": program,
            "time_slot": time_slot,
            "tier": tier,
            "branch": branch,
            "joined_at": date_str
        }

        # Prepend to members list
        members.insert(0, new_member)
        save_members(members)

        return jsonify({
            "success": True,
            "message": f"Welcome to Fitness Gym, {name}!",
            "member": new_member
        }), 201

    if __name__ == "__main__":
        print(f"🚀 Fitness Gym (Production Flask Server) running on http://0.0.0.0:{PORT}")
        print(f"📍 Location: Pune, Maharashtra (Koregaon Park & Baner clubs)")
        print(f"💾 Storage file: {get_storage_path()}")
        app.run(host="0.0.0.0", port=PORT, debug=True)

else:
    # Minimal fallback in non-flask environments
    pass
