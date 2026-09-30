from flask import Flask, render_template, url_for

from config import Config, db

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)
app.config.from_object(Config)

db.init_app(app)

# Import models and routes
from models import *
from routes import *

app.register_blueprint(admin_bp)
app.register_blueprint(buyer_bp)
app.register_blueprint(farmer_bp)
app.register_blueprint(auth_bp)

from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    admin_email = "admin@tmk.com"
    admin_user = User.query.filter_by(email=admin_email).first()
    if not admin_user:
        admin_user = User(
            name="System Admin",
            email=admin_email,
            password_hash=generate_password_hash("admin123"),
            role="admin",
            status="active"
        )
        db.session.add(admin_user)
        db.session.commit()

@app.route("/")
def home():
    return render_template('index.html')

from flask import jsonify

@app.route("/api/auction/<int:auction_id>/status")
def auction_status_api(auction_id):
    auction = Auction.query.get_or_404(auction_id)
    bids = Bid.query.filter_by(auction_id=auction.id).order_by(Bid.bid_amount.desc()).all()
    
    bids_data = []
    for b in bids:
        bids_data.append({
            "id": b.id,
            "bidder_name": b.buyer.business_name or b.buyer.user.name if b.buyer else "Buyer",
            "bid_amount": float(b.bid_amount),
            "bid_time": b.bid_time.strftime("%H:%M:%S") if b.bid_time else "",
            "status": b.status
        })

    return jsonify({
        "auction_id": auction.id,
        "status": auction.status,
        "starting_price": float(auction.starting_price),
        "current_highest_bid": float(auction.current_highest_bid or auction.starting_price),
        "highest_bidder": auction.highest_bidder.business_name if auction.highest_bidder else None,
        "end_time_iso": auction.end_time.isoformat() if auction.end_time else "",
        "bids_count": len(bids),
        "bids": bids_data
    })

if __name__ == "__main__":
    app.run(debug=True)