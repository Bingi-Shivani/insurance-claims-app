from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
app.secret_key = "change-this-secret-key-before-deployment"

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "insurance_claims.db"


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS claims (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                email TEXT NOT NULL,
                policy_number TEXT NOT NULL,
                policy_active INTEGER NOT NULL,
                claim_type TEXT NOT NULL,
                claim_amount REAL NOT NULL,
                description TEXT NOT NULL,
                decision TEXT NOT NULL,
                reason TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        db.commit()


def review_claim(policy_active, claim_amount, previous_claims):
    """
    Demonstration decision engine.
    These are example business rules, not real insurance underwriting rules.
    """
    if not policy_active:
        return "Rejected", "Policy is inactive."
    if claim_amount <= 0:
        return "Rejected", "Claim amount must be greater than zero."
    if claim_amount > 100000:
        return "Escalated", "High-value claim requires manual review."
    if previous_claims >= 3:
        return "Escalated", "Customer has multiple previous claims; manual review required."
    return "Approved", "Claim passed the configured demonstration checks."


@app.route("/")
def index():
    with get_db() as db:
        claims = db.execute(
            "SELECT * FROM claims ORDER BY id DESC"
        ).fetchall()

        totals = db.execute("""
            SELECT
                COUNT(*) AS total,
                SUM(CASE WHEN decision = 'Approved' THEN 1 ELSE 0 END) AS approved,
                SUM(CASE WHEN decision = 'Rejected' THEN 1 ELSE 0 END) AS rejected,
                SUM(CASE WHEN decision = 'Escalated' THEN 1 ELSE 0 END) AS escalated
            FROM claims
        """).fetchone()

    return render_template("index.html", claims=claims, totals=totals)


@app.route("/submit", methods=["GET", "POST"])
def submit_claim():
    if request.method == "POST":
        customer_name = request.form.get("customer_name", "").strip()
        email = request.form.get("email", "").strip()
        policy_number = request.form.get("policy_number", "").strip()
        policy_active = 1 if request.form.get("policy_active") == "on" else 0
        claim_type = request.form.get("claim_type", "").strip()
        description = request.form.get("description", "").strip()

        try:
            claim_amount = float(request.form.get("claim_amount", "0"))
        except ValueError:
            flash("Please enter a valid claim amount.", "error")
            return redirect(url_for("submit_claim"))

        if not all([customer_name, email, policy_number, claim_type, description]):
            flash("Please complete all required fields.", "error")
            return redirect(url_for("submit_claim"))

        if claim_amount <= 0:
            flash("Claim amount must be greater than zero.", "error")
            return redirect(url_for("submit_claim"))

        with get_db() as db:
            previous_claims = db.execute(
                "SELECT COUNT(*) FROM claims WHERE email = ?",
                (email,)
            ).fetchone()[0]

            decision, reason = review_claim(
                policy_active, claim_amount, previous_claims
            )

            cursor = db.execute("""
                INSERT INTO claims (
                    customer_name, email, policy_number, policy_active,
                    claim_type, claim_amount, description, decision,
                    reason, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                customer_name, email, policy_number, policy_active,
                claim_type, claim_amount, description, decision,
                reason, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            claim_id = cursor.lastrowid
            db.commit()

        flash(f"Claim submitted. Automated result: {decision}.", "success")
        return redirect(url_for("claim_details", claim_id=claim_id))

    return render_template("submit_claim.html")


@app.route("/claim/<int:claim_id>")
def claim_details(claim_id):
    with get_db() as db:
        claim = db.execute(
            "SELECT * FROM claims WHERE id = ?", (claim_id,)
        ).fetchone()

        if claim is None:
            flash("Claim not found.", "error")
            return redirect(url_for("index"))

        history = db.execute("""
            SELECT id, claim_type, claim_amount, decision, created_at
            FROM claims
            WHERE email = ? AND id != ?
            ORDER BY id DESC
        """, (claim["email"], claim_id)).fetchall()

    return render_template(
        "claim_details.html", claim=claim, history=history
    )


if __name__ == "__main__":
    init_db()
    # host=0.0.0.0 is required when the app runs inside Docker.
    app.run(host="0.0.0.0", port=5002, debug=True)
