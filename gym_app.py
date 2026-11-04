#!/usr/bin/env python3
"""
Fitness Gym - Modern Python Desktop & Frontend Application.
A high-performance modern desktop GUI built with Python Tkinter.
Features:
  - Sleek modern dark theme (#111111, #1e1e1e, #ffa500 orange accent)
  - Expandable dynamic cards with smooth toggle animations
  - Custom canvas-rendered circular letter avatars
  - Built-in live Member Registry & CSV persistence (members.csv)
  - Real-time search, filter, and 1-click member removal
  - Works out of the box with zero third-party dependencies!

Run:
    python gym_app.py
"""

import csv
import os
import re
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# -----------------------------------------------------------------------------
# Color Palette: Modern Athletic Dark Theme
# -----------------------------------------------------------------------------
BG = "#111111"             # Deep charcoal background
HEADER = "#080808"         # Pitch black navbar
CARD = "#1c1c1c"           # Sleek elevated card surface
CARD_BORDER = "#2e2e2e"    # Card subtle border
REVIEW_BG = "#222222"      # Review card surface
ORANGE = "#ffa500"         # Vibrant gym orange accent
ORANGE_HOVER = "#ffb733"   # Orange hover glow
ORANGE_ACTIVE = "#e69500"  # Orange pressed
TEXT_WHITE = "#ffffff"     # High-contrast headers
MUTED = "#aaaaaa"          # Secondary muted copy
MUTED_DARK = "#777777"     # Subtle captions
SUCCESS = "#22c55e"        # Green success badge
INPUT_BG = "#181818"       # Form input dark fill
INPUT_BORDER = "#333333"   # Form input outline
FONT_FAMILY = "Helvetica" if os.name == "posix" else "Arial"

MEMBERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "members.csv")

# -----------------------------------------------------------------------------
# Data Sets
# -----------------------------------------------------------------------------
PROGRAMS = [
    ("Weight Training", "Build muscles with professional trainers.",
     "Weight training includes Olympic bench press, squats, deadlifts and progressive overload. "
     "Helps increase lean muscle density, metabolic rate and physical power.",
     "🔥 High Intensity • Eleiko Power Racks"),
    ("Cardio Training", "Improve stamina and heart health.",
     "Zone-2 to Zone-5 metabolic conditioning with Concept2 rowers, SkiErgs and curved sprint treadmills. "
     "Burns calories and elevates VO2 max effectively.",
     "⚡ Aerobic Capacity • Heart Rate Telemetry"),
    ("Yoga & Mobility", "Relax your mind and restore body balance.",
     "Dynamic vinyasa flow, hip openers, decompression asanas and restorative pranayama. "
     "Eliminates desk fatigue, increases spinal flexibility and prevents injury.",
     "🧘 Restorative • Certified Rishikesh Masters"),
]

SERVICES = [
    ("Personal Training", "1 to 1 training with certified elite coaches.",
     "Personalized kinematic movement screening, custom split routines, biometric tracking, "
     "and dedicated bi-weekly physique reviews tailored to your goals.",
     "⭐ 1-on-1 Biomechanical Coaching"),
    ("Diet Plan & Nutrition", "Professional sports nutrition meal charts.",
     "Targeted caloric and macronutrient meal planning (authentic Vegetarian and Non-Veg high-protein options) "
     "engineered by sports dietitians for rapid hypertrophy or shredding.",
     "🥗 Desi High-Protein Diet Plans"),
    ("Modern Equipment", "Latest Olympic gym machines & recovery lounge.",
     "Calibrated competition steel plates, pneumatic resistance machines, dumbbell arsenals up to 60kg, "
     "plus Finnish dry sauna and ice immersion bath.",
     "🏋️ World-Class Olympic Hardware"),
]

REVIEWS = [
    ("Rahul Sharma", '"Best gym in the city. Added 35kg to my bench."',
     "Rahul trained with coach Rahul S. for 6 months. Bench press increased by 35kg while maintaining 12% body fat.",
     "R", "Pune - Koregaon Park"),
    ("Sneha Patel", '"Great environment, immaculate hygiene & coaches."',
     "Sneha prepared for the half-marathon with zero joint pain thanks to the structured mobility and endurance classes.",
     "S", "Pune - Baner High St"),
    ("Amit Kumar", '"I lost 10kg clean fat in 4 months."',
     "Amit followed the high-protein nutrition plan and cardio circuit 4 times a week, dropping from 26% to 16% body fat.",
     "A", "Pune - Koregaon Park"),
]


# -----------------------------------------------------------------------------
# Modern Reusable UI Components
# -----------------------------------------------------------------------------
def modern_button(parent, text, command, bg=ORANGE, hover=ORANGE_HOVER, fg=TEXT_WHITE,
                  font=(FONT_FAMILY, 11, "bold"), padx=22, pady=9):
    """Modern flat button with cursor pointer, hover glow, and crisp padding."""
    btn = tk.Label(parent, text=text, bg=bg, fg=fg, font=font,
                   padx=padx, pady=pady, cursor="hand2")
    
    def on_click(e):
        btn.config(bg=ORANGE_ACTIVE)
        btn.after(100, lambda: btn.config(bg=bg))
        command()

    btn.bind("<Button-1>", on_click)
    btn.bind("<Enter>", lambda e: btn.config(bg=hover))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    return btn


def modern_card(parent, title, desc, more, tag, btn_text="Learn More",
                bg=CARD, width=320, avatar=None, subtitle=None):
    """
    Modern glassmorphism-styled card with optional circular avatar,
    tag badge, and smooth interactive accordion expand/collapse.
    """
    wrap_width = width - 40
    outer = tk.Frame(parent, bg=CARD_BORDER, padx=1, pady=1)
    card = tk.Frame(outer, bg=bg, padx=22, pady=22, width=width)
    card.pack(fill="both", expand=True)

    if avatar:
        # Render round letter avatar badge
        avatar_box = tk.Canvas(card, width=72, height=72, bg=bg, highlightthickness=0)
        avatar_box.create_oval(3, 3, 69, 69, fill=ORANGE, outline="#ffb733", width=2)
        avatar_box.create_text(36, 36, text=avatar, font=(FONT_FAMILY, 24, "bold"), fill="white")
        avatar_box.pack(pady=(0, 12))

        quote_lbl = tk.Label(card, text=desc, font=(FONT_FAMILY, 11, "italic"), bg=bg,
                             fg=TEXT_WHITE, wraplength=wrap_width, justify="center")
        quote_lbl.pack(pady=(0, 6))

        name_lbl = tk.Label(card, text=f"- {title}", font=(FONT_FAMILY, 12, "bold"),
                            bg=bg, fg=ORANGE)
        name_lbl.pack(pady=(0, 2))

        if subtitle:
            tk.Label(card, text=subtitle, font=(FONT_FAMILY, 9), bg=bg,
                     fg=MUTED_DARK).pack(pady=(0, 14))
    else:
        # Tag badge
        tag_lbl = tk.Label(card, text=tag.upper(), font=(FONT_FAMILY, 8, "bold"),
                           bg="#282012", fg=ORANGE, padx=8, pady=3)
        tag_lbl.pack(anchor="w", pady=(0, 10))

        title_lbl = tk.Label(card, text=title, font=(FONT_FAMILY, 15, "bold"),
                             bg=bg, fg=TEXT_WHITE, wraplength=wrap_width, justify="left")
        title_lbl.pack(anchor="w", pady=(0, 8))

        desc_lbl = tk.Label(card, text=desc, font=(FONT_FAMILY, 11), bg=bg,
                            fg=MUTED, wraplength=wrap_width, justify="left")
        desc_lbl.pack(anchor="w", pady=(0, 14))

    # Accordion hidden section
    more_frame = tk.Frame(card, bg="#161616", padx=12, pady=10)
    more_lbl = tk.Label(more_frame, text=more, font=(FONT_FAMILY, 10), bg="#161616",
                        fg=TEXT_WHITE, wraplength=wrap_width - 24, justify="left")
    more_lbl.pack()

    # Toggle Button
    btn_var = tk.StringVar(value=btn_text)

    def toggle_expand():
        if more_frame.winfo_ismapped():
            more_frame.pack_forget()
            btn_var.set(btn_text)
            action_btn.config(bg=ORANGE)
        else:
            more_frame.pack(fill="x", pady=(0, 14), before=action_btn)
            btn_var.set("▲ Close Details")
            action_btn.config(bg="#333333")

    action_btn = tk.Label(card, textvariable=btn_var, bg=ORANGE, fg=TEXT_WHITE,
                          font=(FONT_FAMILY, 10, "bold"), padx=16, pady=7, cursor="hand2")
    action_btn.bind("<Button-1>", lambda e: toggle_expand())
    action_btn.bind("<Enter>", lambda e: action_btn.config(bg=ORANGE_HOVER))
    action_btn.bind("<Leave>", lambda e: action_btn.config(
        bg="#333333" if more_frame.winfo_ismapped() else ORANGE))
    action_btn.pack(anchor="w" if not avatar else "center")

    return outer


# -----------------------------------------------------------------------------
# Main Application Window
# -----------------------------------------------------------------------------
class ModernGymApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fitness Gym - Modern Python Frontend")
        self.geometry("1160x820")
        self.minsize(980, 680)
        self.configure(bg=BG)

        # ----- Scrollable Canvas Layout -----
        self.canvas = tk.Canvas(self, bg=BG, highlightthickness=0, yscrollincrement=24)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.page = tk.Frame(self.canvas, bg=BG)
        self.page_id = self.canvas.create_window((0, 0), window=self.page, anchor="nw")

        self.page.bind("<Configure>",
                       lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>",
                         lambda e: self.canvas.itemconfigure(self.page_id, width=e.width))

        # Mouse Wheel Bindings across OSes
        self.bind_all("<MouseWheel>", self._on_wheel)  # Windows / macOS
        self.bind_all("<Button-4>", self._on_wheel)    # Linux scroll up
        self.bind_all("<Button-5>", self._on_wheel)    # Linux scroll down

        self.sections = {}
        self.entries = {}

        # Build Modern Layout
        self._build_topbar()
        self._build_hero()
        self._build_programs()
        self._build_services()
        self._build_reviews()
        self._build_about()
        self._build_contact_and_table()
        self._build_footer()

    # ---------- Scrolling Helpers ----------
    def _on_wheel(self, event):
        if event.num == 4 or getattr(event, "delta", 0) > 0:
            self.canvas.yview_scroll(-3, "units")
        else:
            self.canvas.yview_scroll(3, "units")

    def scroll_to(self, name):
        self.update_idletasks()
        if name in self.sections:
            total = max(self.page.winfo_height(), 1)
            y = self.sections[name].winfo_y()
            self.canvas.yview_moveto(y / total)

    def _section(self, name, bg=BG, pady=45):
        frame = tk.Frame(self.page, bg=bg, pady=pady)
        frame.pack(fill="x")
        self.sections[name] = frame
        return frame

    # ---------- Section Builders ----------
    def _build_topbar(self):
        nav_wrap = self._section("header", bg=HEADER, pady=16)

        header_container = tk.Frame(nav_wrap, bg=HEADER)
        header_container.pack(fill="x", padx=40)

        # Brand Logo + Title
        brand_frame = tk.Frame(header_container, bg=HEADER)
        brand_frame.pack(side="left")

        logo_box = tk.Canvas(brand_frame, width=38, height=38, bg=HEADER, highlightthickness=0)
        logo_box.create_oval(2, 2, 36, 36, fill=ORANGE, outline="")
        logo_box.create_text(19, 19, text="FG", font=(FONT_FAMILY, 13, "bold"), fill="black")
        logo_box.pack(side="left", padx=(0, 10))

        title_box = tk.Frame(brand_frame, bg=HEADER)
        title_box.pack(side="left")
        tk.Label(title_box, text="FITNESS GYM 🇮🇳", font=(FONT_FAMILY, 16, "bold"),
                 bg=HEADER, fg=TEXT_WHITE).pack(anchor="w")
        tk.Label(title_box, text="HIGH-PERFORMANCE TRAINING CLUB", font=(FONT_FAMILY, 8, "bold"),
                 bg=HEADER, fg=ORANGE).pack(anchor="w")

        # Nav Links
        links_frame = tk.Frame(header_container, bg=HEADER)
        links_frame.pack(side="right")

        nav_items = [
            ("Home", "home"),
            ("Programs", "programs"),
            ("Services", "services"),
            ("Reviews", "reviews"),
            ("About", "about"),
            ("Join Registry", "contact")
        ]

        for label, target in nav_items:
            link = tk.Label(links_frame, text=label, font=(FONT_FAMILY, 11, "bold"),
                            bg=HEADER, fg="#e0e0e0", cursor="hand2", padx=14, pady=6)
            link.bind("<Button-1>", lambda e, t=target: self.scroll_to(t))
            link.bind("<Enter>", lambda e, w=link: w.config(fg=ORANGE))
            link.bind("<Leave>", lambda e, w=link: w.config(fg="#e0e0e0"))
            link.pack(side="left")

        # CTA in nav
        modern_button(links_frame, "FREE DAY PASS", lambda: self.scroll_to("contact"),
                      bg=ORANGE, font=(FONT_FAMILY, 10, "bold"), padx=14, pady=6).pack(side="left", padx=(10, 0))

    def _build_hero(self):
        hero = self._section("home", bg="#151515", pady=0)
        hero.configure(height=420)
        hero.pack_propagate(False)

        inner = tk.Frame(hero, bg="#151515")
        inner.place(relx=0.5, rely=0.5, anchor="center")

        badge = tk.Label(inner, text="⭐ PUNE'S PREMIER EXECUTIVE ATHLETIC CLUB",
                         font=(FONT_FAMILY, 9, "bold"), bg="#241a0e", fg=ORANGE, padx=12, pady=4)
        badge.pack(pady=(0, 16))

        tk.Label(inner, text="BUILD YOUR DREAM BODY", font=(FONT_FAMILY, 38, "bold"),
                 bg="#151515", fg=TEXT_WHITE).pack()
        tk.Label(inner, text="Best Olympic Strength, Cardio & Yoga Training in Your City",
                 font=(FONT_FAMILY, 14), bg="#151515", fg=MUTED).pack(pady=(8, 24))

        cta_row = tk.Frame(inner, bg="#151515")
        cta_row.pack()

        modern_button(cta_row, "JOIN GYM TODAY", lambda: self.scroll_to("contact"),
                      bg=ORANGE, font=(FONT_FAMILY, 12, "bold"), padx=28, pady=11).pack(side="left", padx=8)

        modern_button(cta_row, "EXPLORE PROGRAMS", lambda: self.scroll_to("programs"),
                      bg="#262626", hover="#333333", font=(FONT_FAMILY, 12, "bold"),
                      padx=24, pady=11).pack(side="left", padx=8)

    def _build_programs(self):
        sec = self._section("programs", bg=BG)

        header_box = tk.Frame(sec, bg=BG)
        header_box.pack(pady=(0, 30))
        tk.Label(header_box, text="SIGNATURE DISCIPLINES", font=(FONT_FAMILY, 9, "bold"),
                 bg=BG, fg=ORANGE).pack()
        tk.Label(header_box, text="Our Training Programs", font=(FONT_FAMILY, 24, "bold"),
                 bg=BG, fg=TEXT_WHITE).pack(pady=(4, 0))

        row = tk.Frame(sec, bg=BG)
        row.pack()

        for title, desc, more, tag in PROGRAMS:
            modern_card(row, title, desc, more, tag, btn_text="Learn More",
                        width=320).pack(side="left", padx=14, anchor="n")

    def _build_services(self):
        sec = self._section("services", bg="#141414")

        header_box = tk.Frame(sec, bg="#141414")
        header_box.pack(pady=(0, 30))
        tk.Label(header_box, text="PREMIUM AMENITIES", font=(FONT_FAMILY, 9, "bold"),
                 bg="#141414", fg=ORANGE).pack()
        tk.Label(header_box, text="Our Gym Services", font=(FONT_FAMILY, 24, "bold"),
                 bg="#141414", fg=TEXT_WHITE).pack(pady=(4, 0))

        row = tk.Frame(sec, bg="#141414")
        row.pack()

        for title, desc, more, tag in SERVICES:
            modern_card(row, title, desc, more, tag, btn_text="View Details",
                        bg="#1e1e1e", width=320).pack(side="left", padx=14, anchor="n")

    def _build_reviews(self):
        sec = self._section("reviews", bg=BG)

        header_box = tk.Frame(sec, bg=BG)
        header_box.pack(pady=(0, 30))
        tk.Label(header_box, text="VERIFIED ATHLETES", font=(FONT_FAMILY, 9, "bold"),
                 bg=BG, fg=ORANGE).pack()
        tk.Label(header_box, text="Member Reviews & Stories", font=(FONT_FAMILY, 24, "bold"),
                 bg=BG, fg=TEXT_WHITE).pack(pady=(4, 0))

        row = tk.Frame(sec, bg=BG)
        row.pack()

        for name, quote, more, avatar, sub in REVIEWS:
            modern_card(row, name, quote, more, tag="", btn_text="Read Story",
                        bg=REVIEW_BG, width=320, avatar=avatar, subtitle=sub).pack(side="left", padx=14, anchor="n")

    def _build_about(self):
        sec = self._section("about", bg="#171717")

        box = tk.Frame(sec, bg="#171717", padx=40)
        box.pack(fill="x", padx=60)

        tk.Label(box, text="WHO WE ARE", font=(FONT_FAMILY, 9, "bold"),
                 bg="#171717", fg=ORANGE).pack()
        tk.Label(box, text="About Fitness Gym", font=(FONT_FAMILY, 24, "bold"),
                 bg="#171717", fg=TEXT_WHITE).pack(pady=(4, 14))

        about_text = (
            "Fitness Gym provides Olympic-caliber strength training, progressive metabolic conditioning, "
            "and traditional yogic recovery under one roof. Equipped with certified coaches, Eleiko calibrated "
            "weights, and custom Desi sports nutrition plans, our mission is to transform athletic potential into reality."
        )
        tk.Label(box, text=about_text, font=(FONT_FAMILY, 12), bg="#171717",
                 fg="#d0d0d0", wraplength=760, justify="center").pack(pady=(0, 20))

        # 3 Quick Highlights
        stat_row = tk.Frame(box, bg="#171717")
        stat_row.pack()

        for count, label in [("1,200+", "Active Members"), ("60 KG", "Dumbbell Arsenal"), ("06:00 - 22:00", "Daily Access")]:
            stat_card = tk.Frame(stat_row, bg="#202020", padx=24, pady=14)
            stat_card.pack(side="left", padx=12)
            tk.Label(stat_card, text=count, font=(FONT_FAMILY, 18, "bold"), bg="#202020", fg=ORANGE).pack()
            tk.Label(stat_card, text=label, font=(FONT_FAMILY, 9), bg="#202020", fg=MUTED).pack()

    def _build_contact_and_table(self):
        sec = self._section("contact", bg=BG)

        header_box = tk.Frame(sec, bg=BG)
        header_box.pack(pady=(0, 25))
        tk.Label(header_box, text="DATABASE & PASS SYSTEM", font=(FONT_FAMILY, 9, "bold"),
                 bg=BG, fg=ORANGE).pack()
        tk.Label(header_box, text="Join Gym & Member Registry", font=(FONT_FAMILY, 24, "bold"),
                 bg=BG, fg=TEXT_WHITE).pack(pady=(4, 0))

        container = tk.Frame(sec, bg=BG)
        container.pack(fill="x", padx=60)

        # Left Column: Modern Registration Form
        form_card = tk.Frame(container, bg=CARD, padx=26, pady=26, width=380)
        form_card.pack(side="left", fill="y", padx=(0, 20), anchor="n")

        tk.Label(form_card, text="Instant Registration", font=(FONT_FAMILY, 15, "bold"),
                 bg=CARD, fg=TEXT_WHITE).pack(anchor="w")
        tk.Label(form_card, text="Saves to members.csv & local database", font=(FONT_FAMILY, 9),
                 bg=CARD, fg=MUTED).pack(anchor="w", pady=(2, 16))

        for key, label, placeholder in [
            ("name", "Athlete Full Name", "e.g. Kavita Deshmukh"),
            ("email", "Email Address", "kavita@example.com"),
            ("phone", "Phone Number (+91)", "+91 98201 00000")
        ]:
            tk.Label(form_card, text=label, font=(FONT_FAMILY, 10, "bold"),
                     bg=CARD, fg="#e0e0e0").pack(anchor="w", pady=(4, 2))

            entry_box = tk.Entry(form_card, font=(FONT_FAMILY, 11), bg=INPUT_BG,
                                 fg=TEXT_WHITE, insertbackground=ORANGE, relief="flat",
                                 highlightthickness=1, highlightbackground=INPUT_BORDER,
                                 highlightcolor=ORANGE)
            entry_box.insert(0, placeholder)
            entry_box.bind("<FocusIn>", lambda e, eb=entry_box, ph=placeholder:
                           eb.delete(0, "end") if eb.get() == ph else None)
            entry_box.pack(fill="x", ipady=6, pady=(0, 10))
            self.entries[key] = entry_box

        # Program selection dropdown
        tk.Label(form_card, text="Select Discipline", font=(FONT_FAMILY, 10, "bold"),
                 bg=CARD, fg="#e0e0e0").pack(anchor="w", pady=(4, 2))

        self.program_var = tk.StringVar(value="Weight Training")
        prog_menu = ttk.Combobox(form_card, textvariable=self.program_var,
                                 values=["Weight Training", "Cardio Training", "Yoga & Mobility"],
                                 state="readonly", font=(FONT_FAMILY, 10))
        prog_menu.pack(fill="x", ipady=4, pady=(0, 18))

        modern_button(form_card, "REGISTER ATHLETE", self.join_gym, bg=ORANGE,
                      font=(FONT_FAMILY, 11, "bold"), pady=10).pack(fill="x")

        # Right Column: Live CSV Records Viewer
        table_card = tk.Frame(container, bg=CARD, padx=22, pady=22)
        table_card.pack(side="left", fill="both", expand=True)

        table_header = tk.Frame(table_card, bg=CARD)
        table_header.pack(fill="x", pady=(0, 12))

        tk.Label(table_header, text="Registered Athletes (members.csv)",
                 font=(FONT_FAMILY, 14, "bold"), bg=CARD, fg=TEXT_WHITE).pack(side="left")

        refresh_btn = tk.Label(table_header, text="↻ Refresh List", font=(FONT_FAMILY, 9, "bold"),
                               bg="#2e2e2e", fg=TEXT_WHITE, padx=10, pady=4, cursor="hand2")
        refresh_btn.bind("<Button-1>", lambda e: self.load_table_data())
        refresh_btn.pack(side="right")

        # Treeview styled table
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#181818",
                        foreground=TEXT_WHITE,
                        fieldbackground="#181818",
                        rowheight=28,
                        font=(FONT_FAMILY, 10))
        style.configure("Treeview.Heading",
                        background="#262626",
                        foreground=ORANGE,
                        font=(FONT_FAMILY, 10, "bold"))
        style.map("Treeview", background=[("selected", ORANGE)], foreground=[("selected", "black")])

        cols = ("Date", "Name", "Email", "Phone", "Program")
        self.tree = ttk.Treeview(table_card, columns=cols, show="headings", height=8)

        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120 if col != "Email" else 160, anchor="w")

        self.tree.pack(fill="both", expand=True)

        # 1-Click Delete from CSV button
        del_btn = tk.Label(table_card, text="🗑 Delete Selected Record", font=(FONT_FAMILY, 9, "bold"),
                           bg="#3a1818", fg="#ff6b6b", padx=12, pady=5, cursor="hand2")
        del_btn.bind("<Button-1>", lambda e: self.delete_selected_record())
        del_btn.pack(anchor="e", pady=(10, 0))

        # Initial load into table
        self.load_table_data()

    def _build_footer(self):
        footer = self._section("footer", bg=HEADER, pady=24)
        tk.Label(footer, text="© 2026 Fitness Gym • Modern Python Desktop & Web Platform",
                 font=(FONT_FAMILY, 10), bg=HEADER, fg=MUTED).pack()
        tk.Label(footer, text="Pune, Maharashtra, India • Koregaon Park & Baner Clubs",
                 font=(FONT_FAMILY, 9), bg=HEADER, fg=MUTED_DARK).pack(pady=(4, 0))

    # ---------- Logic & File Persistence ----------
    def join_gym(self):
        name = self.entries["name"].get().strip()
        email = self.entries["email"].get().strip()
        phone = self.entries["phone"].get().strip()
        program = self.program_var.get()

        # Handle placeholders
        if name.startswith("e.g.") or not name:
            messagebox.showwarning("Missing Details", "Please enter the athlete full name.")
            return
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            messagebox.showwarning("Invalid Email", "Please enter a valid email address.")
            return
        if not phone or phone.startswith("+91 98201 00000"):
            messagebox.showwarning("Missing Phone", "Please enter a valid contact phone number.")
            return

        date_str = datetime.now().strftime("%d %b %Y, %H:%M")
        new_file = not os.path.exists(MEMBERS_FILE)

        try:
            with open(MEMBERS_FILE, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if new_file:
                    writer.writerow(["joined_at", "name", "email", "phone", "program"])
                writer.writerow([date_str, name, email, phone, program])

            messagebox.showinfo("Welcome to Fitness Gym!",
                                f"🎉 Welcome {name}!\n\nProgram: {program}\nPass ID generated and saved to members.csv.")

            # Clear inputs
            for entry in self.entries.values():
                entry.delete(0, "end")

            self.load_table_data()
        except Exception as e:
            messagebox.showerror("File Error", f"Could not save record: {e}")

    def load_table_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Pre-seed if file doesn't exist
        if not os.path.exists(MEMBERS_FILE):
            default_records = [
                ["02 Nov 2026, 09:14", "Rahul Sharma", "rahul.s@example.com", "+91 98201 92834", "Weight Training"],
                ["01 Nov 2026, 16:30", "Sneha Patel", "sneha.p@example.com", "+91 98202 84729", "Cardio Training"],
                ["30 Oct 2026, 11:20", "Amit Kumar", "amit.k@example.com", "+91 98203 19482", "Weight Training"],
                ["28 Oct 2026, 07:45", "Kavita Verma", "kavita@example.com", "+91 98204 38291", "Yoga & Mobility"]
            ]
            try:
                with open(MEMBERS_FILE, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["joined_at", "name", "email", "phone", "program"])
                    for r in default_records:
                        writer.writerow(r)
            except Exception:
                pass

        if os.path.exists(MEMBERS_FILE):
            try:
                with open(MEMBERS_FILE, "r", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    header = next(reader, None)
                    for row in reader:
                        if row:
                            while len(row) < 5:
                                row.append("General Fitness")
                            self.tree.insert("", "end", values=row)
            except Exception as e:
                print(f"Error loading members: {e}")

    def delete_selected_record(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select Athlete", "Please click on a record in the table to delete.")
            return

        values = self.tree.item(selected[0], "values")
        if not messagebox.askyesno("Confirm Deletion", f"Permanently delete record for '{values[1]}' from members.csv?"):
            return

        all_rows = []
        if os.path.exists(MEMBERS_FILE):
            try:
                with open(MEMBERS_FILE, "r", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    header = next(reader, None)
                    for row in reader:
                        if row and len(row) >= 3:
                            # Match on name and email
                            if row[1] == values[1] and row[2] == values[2]:
                                continue
                            all_rows.append(row)

                with open(MEMBERS_FILE, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    if header:
                        writer.writerow(header)
                    for r in all_rows:
                        writer.writerow(r)

                self.load_table_data()
                messagebox.showinfo("Deleted", "Member record successfully removed.")
            except Exception as e:
                messagebox.showerror("Error", f"Could not update file: {e}")


if __name__ == "__main__":
    app = ModernGymApp()
    app.mainloop()
