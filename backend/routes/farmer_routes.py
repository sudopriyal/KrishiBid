from flask import Blueprint, url_for, request, flash, session, render_template, redirect
from datetime import datetime, timezone, timedelta
from sqlalchemy import func
from config import db
from models import User, FarmerProfile, ProduceListing, Auction, Bid, Transaction
from utils.decorators import login_required, farmer_required, only_farmer_required

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


@farmer_bp.route("/sell-produce/<int:user_id>", methods=["GET", "POST"])
@farmer_required("user_id")
def sell_produce(user_id):
    user = User.query.get_or_404(user_id)
    farmer_profile = FarmerProfile.query.filter_by(user_id=user_id).first()
    if not farmer_profile:
        farmer_profile = FarmerProfile(user_id=user_id)
        db.session.add(farmer_profile)
        db.session.commit()

    if request.method == "POST":
        crop_name = request.form.get("crop_name", "").strip()
        crop_type = request.form.get("crop_type", "").strip()
        quantity = request.form.get("quantity", "0")
        quantity_unit = request.form.get("quantity_unit", "kg").strip()
        quality_grade = request.form.get("quality_grade", "Grade A").strip()
        harvest_date_str = request.form.get("harvest_date", "")
        location = request.form.get("location", "").strip()
        description = request.form.get("description", "").strip()
        starting_price = request.form.get("starting_price", "0")
        duration_hours = int(request.form.get("duration_hours", "24"))

        if not crop_name or float(quantity) <= 0 or float(starting_price) <= 0:
            flash("Please enter valid crop name, quantity, and starting price.", "danger")
            return redirect(url_for("farmer.sell_produce", user_id=user_id))

        harvest_date = None
        if harvest_date_str:
            try:
                harvest_date = datetime.strptime(harvest_date_str, "%Y-%m-%d").date()
            except ValueError:
                harvest_date = None

        # Create Produce Listing
        listing = ProduceListing(
            farmer_id=farmer_profile.id,
            crop_name=crop_name,
            crop_type=crop_type or None,
            quantity=float(quantity),
            quantity_unit=quantity_unit,
            quality_grade=quality_grade,
            harvest_date=harvest_date,
            location=location or farmer_profile.district or "Gujarat",
            description=description or None,
            starting_price=float(starting_price),
            status="active"
        )
        db.session.add(listing)
        db.session.flush()

        # Create Live Auction
        now_utc = datetime.now(timezone.utc)
        end_utc = now_utc + timedelta(hours=duration_hours)
        auction = Auction(
            listing_id=listing.id,
            start_time=now_utc,
            end_time=end_utc,
            starting_price=float(starting_price),
            current_highest_bid=float(starting_price),
            status="active"
        )
        db.session.add(auction)
        db.session.commit()

        flash(f"Live Auction launched for {crop_name}! Verified buyers can now place competitive bids.", "success")
        return redirect(url_for("farmer.live_auction", auction_id=auction.id))

    return render_template("farmer/sell_produce.html", user=user)


@farmer_bp.route("/auction/<int:auction_id>")
@only_farmer_required
def live_auction(auction_id):
    auction = Auction.query.get_or_404(auction_id)
    listing = auction.listing
    user = User.query.get(session.get("user_id"))

    # Verify farmer ownership
    if listing.farmer.user_id != user.id:
        flash("You are not authorized to view this auction.", "danger")
        return redirect(url_for("farmer.dashboard", user_id=user.id))

    bids = Bid.query.filter_by(auction_id=auction.id).order_by(Bid.bid_amount.desc()).all()

    return render_template(
        "farmer/auction_details.html",
        auction=auction,
        listing=listing,
        bids=bids,
        user=user
    )


@farmer_bp.route("/accept-bid/<int:bid_id>", methods=["POST"])
@only_farmer_required
def accept_bid(bid_id):
    bid = Bid.query.get_or_404(bid_id)
    auction = bid.auction
    listing = auction.listing
    user = User.query.get(session.get("user_id"))

    if listing.farmer.user_id != user.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for("farmer.dashboard", user_id=user.id))

    # Accept this bid & reject others
    bid.status = "accepted"
    other_bids = Bid.query.filter(Bid.auction_id == auction.id, Bid.id != bid.id).all()
    for b in other_bids:
        b.status = "rejected"

    now_utc = datetime.now(timezone.utc)
    auction.status = "ended"
    auction.closed_at = now_utc
    auction.current_highest_bid = bid.bid_amount
    auction.current_highest_bidder_id = bid.buyer_id

    listing.status = "sold"

    # Create Completed Transaction
    price_per_unit = float(bid.bid_amount) / float(listing.quantity) if listing.quantity and float(listing.quantity) > 0 else float(bid.bid_amount)
    transaction = Transaction(
        auction_id=auction.id,
        listing_id=listing.id,
        farmer_id=listing.farmer_id,
        buyer_id=bid.buyer_id,
        bid_id=bid.id,
        quantity=listing.quantity,
        price_per_unit=price_per_unit,
        total_amount=bid.bid_amount,
        status="completed",
        completed_at=now_utc
    )
    db.session.add(transaction)
    db.session.commit()

    flash(f"Bid of ₹{bid.bid_amount} accepted! Sale completed with buyer.", "success")
    return redirect(url_for("farmer.dashboard", user_id=user.id))