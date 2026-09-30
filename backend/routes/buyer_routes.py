from flask import Blueprint, url_for, request, flash, session, render_template, redirect
from datetime import datetime, timezone
from config import db
from models import User, BuyerProfile, Auction, ProduceListing, Bid, Transaction
from utils.decorators import login_required, buyer_required, only_buyer_required

buyer_bp = Blueprint("buyer", __name__, url_prefix="/buyer")


@buyer_bp.route("/dashboard/<int:user_id>")
@buyer_required("user_id")
def dashboard(user_id):
    user = User.query.get_or_404(user_id)
    buyer_profile = BuyerProfile.query.filter_by(user_id=user_id).first()

    if not buyer_profile:
        buyer_profile = BuyerProfile(user_id=user_id, verification_status="pending")
        db.session.add(buyer_profile)
        db.session.commit()

    search_query = request.args.get("q", "").strip()

    # Query active auctions
    query = Auction.query.join(ProduceListing).filter(Auction.status == "active")
    if search_query:
        query = query.filter(
            (ProduceListing.crop_name.ilike(f"%{search_query}%")) |
            (ProduceListing.location.ilike(f"%{search_query}%"))
        )

    auctions = query.order_by(Auction.created_at.desc()).all()

    return render_template(
        "buyer/dashboard.html",
        user=user,
        buyer=buyer_profile,
        auctions=auctions
    )


@buyer_bp.route("/auction/<int:auction_id>")
@only_buyer_required
def auction_details(auction_id):
    auction = Auction.query.get_or_404(auction_id)
    listing = auction.listing
    user = User.query.get(session.get("user_id"))
    buyer_profile = BuyerProfile.query.filter_by(user_id=user.id).first()

    bids = Bid.query.filter_by(auction_id=auction.id).order_by(Bid.bid_amount.desc()).all()

    return render_template(
        "buyer/auction_details.html",
        auction=auction,
        listing=listing,
        bids=bids,
        buyer=buyer_profile,
        user=user
    )


@buyer_bp.route("/place-bid/<int:auction_id>", methods=["POST"])
@only_buyer_required
def place_bid(auction_id):
    auction = Auction.query.get_or_404(auction_id)
    user_id = session.get("user_id")
    buyer_profile = BuyerProfile.query.filter_by(user_id=user_id).first()

    if not buyer_profile or buyer_profile.verification_status != "approved":
        flash("Your buyer profile must be approved by the admin before placing bids.", "warning")
        return redirect(url_for("buyer.auction_details", auction_id=auction_id))

    if auction.status != "active":
        flash("This live auction is no longer active.", "danger")
        return redirect(url_for("buyer.auction_details", auction_id=auction_id))

    bid_amount_raw = request.form.get("bid_amount", "0")
    try:
        bid_amount = float(bid_amount_raw)
    except ValueError:
        flash("Please enter a valid numeric bid amount.", "danger")
        return redirect(url_for("buyer.auction_details", auction_id=auction_id))

    current_min_bid = float(auction.current_highest_bid or auction.starting_price)
    if bid_amount <= current_min_bid:
        flash(f"Your bid (₹{bid_amount}) must be higher than the current highest bid (₹{current_min_bid}).", "danger")
        return redirect(url_for("buyer.auction_details", auction_id=auction_id))

    # Record Bid
    bid = Bid(
        auction_id=auction.id,
        buyer_id=buyer_profile.id,
        bid_amount=bid_amount,
        status="active"
    )

    # Update Auction State
    auction.current_highest_bid = bid_amount
    auction.current_highest_bidder_id = buyer_profile.id

    db.session.add(bid)
    db.session.commit()

    flash(f"Your bid of ₹{bid_amount} has been placed successfully!", "success")
    return redirect(url_for("buyer.auction_details", auction_id=auction.id))