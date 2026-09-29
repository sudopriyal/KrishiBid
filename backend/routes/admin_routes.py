from flask import Blueprint, render_template, flash, session, redirect, url_for
from datetime import datetime
from config import db
from models import User, FarmerProfile, BuyerProfile
from utils.decorators import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    total_farmers = FarmerProfile.query.count()
    total_buyers = BuyerProfile.query.count()
    pending_verifications = BuyerProfile.query.filter_by(verification_status="pending").count()
    
    farmers = FarmerProfile.query.join(User).all()
    buyers = BuyerProfile.query.join(User).all()
    
    return render_template(
        "admin/dashboard.html",
        total_farmers=total_farmers,
        total_buyers=total_buyers,
        pending_verifications=pending_verifications,
        farmers=farmers,
        buyers=buyers
    )

@admin_bp.route("/verify-buyer/<int:buyer_id>/<action>", methods=["POST"])
@admin_required
def verify_buyer(buyer_id, action):
    buyer = BuyerProfile.query.get_or_404(buyer_id)
    if action == "approve":
        buyer.verification_status = "approved"
        buyer.verified_at = datetime.utcnow()
        flash(f"Buyer profile for {buyer.business_name or buyer.user.name} approved.", "success")
    elif action == "reject":
        buyer.verification_status = "rejected"
        flash(f"Buyer profile for {buyer.business_name or buyer.user.name} rejected.", "warning")
    db.session.commit()
    return redirect(url_for("admin.dashboard"))