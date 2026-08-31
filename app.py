"""
LEGENDARY GUNDAM ARCHIVE — single-file version.
Everything lives here: data, routes, unlock logic. One template (index.html)
handles every "page" via server-side state — no separate admin/login/profile
files, no static/ folder, no database.

To add/edit Gundam: just edit the GUNDAMS list below and redeploy.
"""

import os
import re
from flask import Flask, render_template, request, session, jsonify, redirect, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-key-change-me")

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "changeme")

CODE_PATTERN = re.compile(r"^GDM-[A-Z0-9]{4}-[A-Z0-9]{4}$")

# ---------------------------------------------------------------------------
# DATA — edit this list to add/remove/update Gundam units.
# ---------------------------------------------------------------------------
GUNDAMS = [
    {
        "id": 1,
        "secret_code": "GDM-X7K9-PQ42",  # TEST DATA
        "name": "RX-78-2 Gundam",
        "youtube_video_id": "dQw4w9WgXcQ",
        "thumbnail": "",
        "description": "The original Gundam. Piloted by Amuro Ray during the One Year War.",
        "battle_history": "Fought in the Battle of Loum, the assault on Solomon, and the final battle of A Baoa Qu.",
        "legendary_moment": "Single-handedly held the line against overwhelming Zeon forces at Solomon.",
        "active": True,
    },
    {
        "id": 2,
        "secret_code": "GDM-8F2M-Z91L",  # TEST DATA
        "name": "MS-06S Zaku II (Char Custom)",
        "youtube_video_id": "dQw4w9WgXcQ",
        "thumbnail": "",
        "description": "The red command variant piloted by Char Aznable, three times faster than a standard Zaku.",
        "battle_history": "Led Zeon assaults across multiple fronts of the One Year War.",
        "legendary_moment": "Outmaneuvered federation forces in a legendary one-on-one duel.",
        "active": True,
    },
]


def find_by_code(code):
    return next((g for g in GUNDAMS if g["secret_code"] == code and g["active"]), None)


def find_by_id(gundam_id):
    return next((g for g in GUNDAMS if g["id"] == gundam_id and g["active"]), None)


def normalize_code(raw):
    return (raw or "").strip().upper()


# ---------------------------------------------------------------------------
# ROUTES
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    view = request.args.get("view", "home")  # home | unlock | admin | login

    if view == "admin":
        if not session.get("is_admin"):
            return redirect(url_for("index", view="login"))
        return render_template("index.html", view="admin", gundams=GUNDAMS)

    if view == "gundam":
        gid = request.args.get("id", type=int)
        gundam = find_by_id(gid) if gid else None
        if not gundam or gid not in session.get("unlocked", []):
            return redirect(url_for("index", view="unlock"))
        return render_template("index.html", view="gundam", gundam=gundam)

    return render_template("index.html", view=view, featured=GUNDAMS[:3])


@app.route("/api/unlock", methods=["POST"])
def api_unlock():
    data = request.get_json(silent=True) or {}
    code = normalize_code(data.get("code"))

    if not CODE_PATTERN.match(code):
        return jsonify(success=False, message="Access denied. Unknown unit code."), 200

    gundam = find_by_code(code)
    if not gundam:
        return jsonify(success=False, message="Access denied. Unknown unit code."), 200

    unlocked = set(session.get("unlocked", []))
    unlocked.add(gundam["id"])
    session["unlocked"] = list(unlocked)

    return jsonify(success=True, gundam_id=gundam["id"])


@app.route("/api/login", methods=["POST"])
def api_login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session["is_admin"] = True
        return redirect(url_for("index", view="admin"))
    return redirect(url_for("index", view="login", error="1"))


@app.route("/api/logout")
def api_logout():
    session.pop("is_admin", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
