from functools import wraps
from flask import session, redirect, url_for, flash


def admin_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            flash("Please log in first.")
            return redirect(url_for("auth.login"))

        if session.get("role") != "admin":
            flash("Access denied.")
            return redirect(url_for("user.dashboard"))

        return func(*args, **kwargs)

    return wrapper


def only_buyer_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            flash("Please log in first.")
            return redirect(url_for("auth.login"))

        if session.get("role") != "buyer":
            flash("Access denied.")
            return redirect(url_for("user.dashboard"))

        return func(*args, **kwargs)

    return wrapper


def buyer_required(route_param):

    def decorator(f):

        @wraps(f)
        def decorated_function(*args, **kwargs):

            if "user_id" not in session:
                flash("Please log in first.")
                return redirect(url_for("auth.login"))

            if session.get("role") != "buyer":
                flash("Access denied.")
                return redirect(url_for("auth.login"))

            if kwargs.get(route_param) != session["user_id"]:
                flash("You are not authorized to access this page.")
                return redirect(
                    url_for(
                        "buyer.dashboard",
                        user_id=session["user_id"]
                    )
                )

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def only_farmer_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            flash("Please log in first.")
            return redirect(url_for("auth.login"))

        if session.get("role") != "farmer":
            flash("Access denied.")
            return redirect(url_for("user.dashboard"))

        return func(*args, **kwargs)

    return wrapper


def farmer_required(route_param):

    def decorator(f):

        @wraps(f)
        def decorated_function(*args, **kwargs):

            if "user_id" not in session:
                flash("Please log in first.")
                return redirect(url_for("auth.login"))

            if session.get("role") != "farmer":
                flash("Access denied.")
                return redirect(url_for("auth.login"))

            if kwargs.get(route_param) != session["user_id"]:
                flash("You are not authorized to access this page.")
                return redirect(
                    url_for(
                        "farmer.dashboard",
                        user_id=session["user_id"]
                    )
                )

            return f(*args, **kwargs)

        return decorated_function

    return decorator

def login_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            flash("Please log in first.")
            return redirect(url_for("auth.login"))

        return func(*args, **kwargs)

    return wrapper