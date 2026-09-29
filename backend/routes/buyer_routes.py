from flask import Blueprint, url_for, request, flash, session, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import db
from models import *
from utils.decorators import login_required, buyer_required, only_buyer_required
from sqlalchemy import func

buyer_bp = Blueprint("buyer", __name__, url_prefix="/buyer")

@buyer_bp.route("/dashboard/<int:user_id>")
@buyer_required("user_id")
def dashboard(user_id):
    return render_template("buyer/dashboard.html")