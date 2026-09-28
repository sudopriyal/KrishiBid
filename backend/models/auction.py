from config import db
from datetime import datetime, timezone
from .enums import auction_status

class Auction(db.Model):
    __tablename__ = "auctions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    listing_id = db.Column(
        db.Integer,
        db.ForeignKey("produce_listings.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    start_time = db.Column(
        db.DateTime(timezone=True),
        nullable=False
    )

    end_time = db.Column(
        db.DateTime(timezone=True),
        nullable=False
    )

    starting_price = db.Column(
        db.Numeric(12, 2),
        nullable=False
    )

    current_highest_bid = db.Column(
        db.Numeric(12, 2),
        nullable=True
    )

    current_highest_bidder_id = db.Column(
        db.Integer,
        db.ForeignKey("buyer_profiles.id", ondelete="SET NULL"),
        nullable=True
    )

    status = db.Column(
        auction_status,
        nullable=False,
        default="scheduled"
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    closed_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True
    )

    # Relationships

    listing = db.relationship(
        "ProduceListing",
        back_populates="auctions"
    )

    highest_bidder = db.relationship(
        "BuyerProfile",
        back_populates="won_auctions"
    )

    bids = db.relationship(
        "Bid",
        back_populates="auction",
        cascade="all, delete-orphan"
    )

    transaction = db.relationship(
        "Transaction",
        back_populates="auction",
        uselist=False
    )