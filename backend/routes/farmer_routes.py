from flask import Blueprint, url_for, request, flash, session, render_template, redirect
from datetime import datetime
from sqlalchemy import func
from config import db
from models import User, FarmerProfile, ProduceListing, Auction, Bid, Transaction
from utils.decorators import login_required, farmer_required

farmer_bp = Blueprint("farmer", __name__, url_prefix="/farmer")

@farmer_bp.route("/dashboard/<int:user_id>")
@farmer_required("user_id")
def dashboard(user_id):
    user = User.query.get_or_404(user_id)
    farmer_profile = FarmerProfile.query.filter_by(user_id=user_id).first()
    
    if not farmer_profile:
        farmer_profile = FarmerProfile(user_id=user_id)
        db.session.add(farmer_profile)
        db.session.commit()

    # Dynamic metrics from real database queries
    active_listings_count = ProduceListing.query.filter_by(
        farmer_id=farmer_profile.id,
        status="active"
    ).count()

    total_earnings = db.session.query(
        func.coalesce(func.sum(Transaction.total_amount), 0)
    ).filter(
        Transaction.farmer_id == farmer_profile.id,
        Transaction.status == "completed"
    ).scalar() or 0

    total_bids_count = db.session.query(
        func.count(Bid.id)
    ).select_from(Bid).join(Auction).join(ProduceListing).filter(
        ProduceListing.farmer_id == farmer_profile.id
    ).scalar() or 0

    completed_sales_count = Transaction.query.filter_by(
        farmer_id=farmer_profile.id,
        status="completed"
    ).count()

    # Produce Listings for this farmer
    listings = ProduceListing.query.filter_by(
        farmer_id=farmer_profile.id
    ).order_by(ProduceListing.created_at.desc()).all()

    # Recent Bids placed on this farmer's listings
    recent_bids = db.session.query(Bid, ProduceListing)\
        .join(Auction, Bid.auction_id == Auction.id)\
        .join(ProduceListing, Auction.listing_id == ProduceListing.id)\
        .filter(ProduceListing.farmer_id == farmer_profile.id)\
        .order_by(Bid.bid_time.desc()).limit(5).all()

    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting = "Good morning"
    elif current_hour < 17:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    return render_template(
        "farmer/dashboard.html",
        user=user,
        farmer=farmer_profile,
        greeting=greeting,
        active_listings_count=active_listings_count,
        total_earnings=float(total_earnings),
        total_bids_count=total_bids_count,
        completed_sales_count=completed_sales_count,
        listings=listings,
        recent_bids=recent_bids
    )

@farmer_bp.route("/sell-produce/<int:user_id>")
@farmer_required("user_id")
def sell_produce(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("farmer/sell_produce.html", user=user)