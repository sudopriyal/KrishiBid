from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from config import db
from models import User, FarmerProfile, BuyerProfile

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        role = request.form.get("role", "").strip().lower()

        if not all([name, email, password, confirm_password, role]):
            flash("Please fill in all required fields.", "danger")
            return redirect(url_for("auth.signup"))

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("auth.signup"))

        if role not in ["farmer", "buyer"]:
            flash("Invalid role selected.", "danger")
            return redirect(url_for("auth.signup"))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("An account with this email already exists.", "danger")
            return redirect(url_for("auth.signup"))

        try:
            user = User(
                name=name,
                email=email,
                phone=phone or None,
                password_hash=generate_password_hash(password),
                role=role,
                status="active"
            )

            db.session.add(user)
            db.session.flush()  # Generates user.id before profile creation

            if role == "farmer":
                profile = FarmerProfile(user_id=user.id)
            else:
                profile = BuyerProfile(
                    user_id=user.id,
                    verification_status="pending"
                )

            db.session.add(profile)
            db.session.commit()

            flash("Account created successfully. Please log in.", "success")
            return redirect(url_for("auth.login"))

        except Exception:
            db.session.rollback()
            flash("Could not create your account. Please try again.", "danger")
            return redirect(url_for("auth.signup"))

    return render_template("auth/signup.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash("Invalid email or password.", "danger")
            return redirect(url_for("auth.login"))

        if user.status != "active":
            flash("Your account is not active. Please contact the administrator.", "warning")
            return redirect(url_for("auth.login"))

        session.clear()
        session["user_id"] = user.id
        session["role"] = user.role
        session["name"] = user.name

        flash(f"Welcome back, {user.name}!", "success")

        if user.role == "admin":
            return redirect(url_for("admin.dashboard"))

        elif user.role == "farmer":
            return redirect(
                url_for(
                    "farmer.dashboard",
                    user_id=user.id
                )
            )

        elif user.role == "buyer":
            return redirect(
                url_for(
                    "buyer.dashboard",
                    user_id=user.id
                )
            )

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for("auth.login"))