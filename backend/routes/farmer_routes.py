from flask import Blueprint, url_for, request, flash, session, render_template, redirect
from datetime import datetime
from config import db
from models import User
from utils.decorators import login_required, farmer_required, only_farmer_required

farmer_bp = Blueprint("farmer", __name__, url_prefix="/farmer")

@farmer_bp.route("/dashboard/<int:user_id>")
@farmer_required("user_id")
def dashboard(user_id):
    user = User.query.get_or_404(user_id)
    
    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting = "Good morning"
    elif current_hour < 17:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    return render_template("farmer/dashboard.html", user=user, greeting=greeting)

@farmer_bp.route("/sell-produce/<int:user_id>")
@farmer_required("user_id")
def sell_produce(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("farmer/sell_produce.html", user=user)