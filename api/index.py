#!/usr/bin/env python3
"""
Vercel Serverless Function - Fitness Gym REST API.
Self-contained Flask WSGI Application optimized for Vercel Serverless Python runtime.
Location: Pune, Maharashtra, India (Koregaon Park & Baner High Street Clubs)
"""

import json
import os
import sys
import csv
import io
from datetime import datetime
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

# -----------------------------------------------------------------------------
# Storage: Uses /tmp in Vercel Serverless to prevent read-only filesystem errors
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
    return "/tmp/members.json"

def load_members():
    global _MEMBERS_CACHE
    if _MEMBERS_CACHE is not None:
        return _MEMBERS_CACHE
    path = get_storage_path()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                _MEMBERS_CACHE = json.load(f)
                return _MEMBERS_CACHE
        except Exception:
            pass
    _MEMBERS_CACHE = list(DEFAULT_SEED_MEMBERS)
    return _MEMBERS_CACHE

def save_members(members):
    global _MEMBERS_CACHE
    _MEMBERS_CACHE = members
    try:
        with open(get_storage_path(), "w", encoding="utf-8") as f:
            json.dump(members, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False

# -----------------------------------------------------------------------------
# Static Data Sets
# -----------------------------------------------------------------------------
PROGRAMS_DATA = [
    {
        "id": "p1",
        "title": "Weight Training",
        "desc": "Build muscles with professional trainers.",
        "more": "Weight training includes Olympic bench press, squats, deadlifts and progressive overload.",
        "tag": "High Intensity • Eleiko Power Racks"
    },
    {
        "id": "p2",
        "title": "Cardio Training",
        "desc": "Improve stamina and heart health.",
        "more": "Zone-2 to Zone-5 metabolic conditioning with Concept2 rowers, SkiErgs and curved sprint treadmills.",
        "tag": "Aerobic Capacity • Heart Rate Telemetry"
    },
    {
        "id": "p3",
        "title": "Yoga & Mobility",
        "desc": "Relax your mind and restore body balance.",
        "more": "Dynamic vinyasa flow, hip openers, decompression asanas and restorative pranayama.",
        "tag": "Restorative • Rishikesh Masters"
    }
]

SERVICES_DATA = [
    {
        "id": "s1",
        "title": "Personal Training",
        "desc": "1 to 1 training with certified elite coaches.",
        "more": "Personalized kinematic movement screening and custom split routines."
    },
    {
        "id": "s2",
        "title": "Diet Plan & Nutrition",
        "desc": "Professional sports nutrition meal charts.",
        "more": "Targeted caloric and macronutrient meal planning for athletes."
    },
    {
        "id": "s3",
        "title": "Modern Equipment",
        "desc": "Latest Olympic gym machines & recovery lounge.",
        "more": "Calibrated competition steel plates, dumbbells up to 60kg, and Finnish sauna."
    }
]

REVIEWS_DATA = [
    {
        "id": "r1",
        "name": "Rahul",
        "avatar": "R",
        "quote": '"Best gym in the city."',
        "more": "Rahul improved strength in 6 months. Bench press increased by 35kg."
    },
    {
        "id": "r2",
        "name": "Sneha",
        "avatar": "S",
        "quote": '"Great environment."',
        "more": "Sneha loves the trainers and equipment. Prepared for the Pune half-marathon."
    },
    {
        "id": "r3",
        "name": "Amit",
        "avatar": "A",
        "quote": '"I lost 10kg."',
        "more": "Amit followed the cardio and diet plan regularly. Dropped 10kg clean fat in 4 months."
    }
]

# -----------------------------------------------------------------------------
# CORS Middleware
# -----------------------------------------------------------------------------
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
    return response

# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------
@app.route("/", methods=["GET", "OPTIONS"])
@app.route("/api", methods=["GET", "OPTIONS"])
@app.route("/api/", methods=["GET", "OPTIONS"])
def index():
    if request.method == "OPTIONS":
        return ("", 204)
    return jsonify({
        "service": "Fitness Gym REST API",
        "platform": "Vercel Serverless Function",
        "status": "healthy",
        "version": "2.4.0",
        "endpoints": [
            "/api/health",
            "/api/programs",
            "/api/services",
            "/api/reviews",
            "/api/members",
            "/join",
            "/api/export"
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
        "environment": "vercel-serverless",
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
        return jsonify({"success": True, "message": "All member records cleared", "count": 0})

    if request.method == "POST":
        data = request.get_json(silent=True) or request.form.to_dict()
        return _create_member(data)

@app.route("/api/members/<member_id>", methods=["GET", "DELETE", "OPTIONS"])
@app.route("/members/<member_id>", methods=["GET", "DELETE", "OPTIONS"])
def handle_single_member(member_id):
    if request.method == "OPTIONS":
        return ("", 204)

    members = load_members()
    matched = [m for m in members if m.get("id") == member_id]

    if not matched:
        return jsonify({"error": f"Member with ID '{member_id}' not found"}), 404

    if request.method == "GET":
        return jsonify(matched[0])

    if request.method == "DELETE":
        updated = [m for m in members if m.get("id") != member_id]
        save_members(updated)
        return jsonify({
            "success": True,
            "message": f"Member {matched[0].get('name')} ({member_id}) was deleted",
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
    writer.writerow(["id", "name", "email", "phone", "program", "time_slot", "tier", "branch", "joined_at"])
    for m in members:
        writer.writerow([
            m.get("id", ""),
            m.get("name", ""),
            m.get("email", ""),
            m.get("phone", ""),
            m.get("program", ""),
            m.get("time_slot", ""),
            m.get("tier", ""),
            m.get("branch", ""),
            m.get("joined_at", "")
        ])
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=members.csv"}
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
    new_id = f"FIT-{1040 + len(members) + 1}"
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

    members.insert(0, new_member)
    save_members(members)

    return jsonify({
        "success": True,
        "message": f"Welcome to Fitness Gym, {name}!",
        "member": new_member
    }), 201
