from config import db
from datetime import datetime, timezone
from .enums import transaction_status

class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    auction_id = db.Column(
        db.Integer,
        db.ForeignKey("auctions.id", ondelete="RESTRICT"),
        nullable=False
    )

    listing_id = db.Column(
        db.Integer,
        db.ForeignKey("produce_listings.id", ondelete="RESTRICT"),
        nullable=False
    )

    farmer_id = db.Column(
        db.Integer,
        db.ForeignKey("farmer_profiles.id", ondelete="RESTRICT"),
        nullable=False
    )

    buyer_id = db.Column(
        db.Integer,
        db.ForeignKey("buyer_profiles.id", ondelete="RESTRICT"),
        nullable=False
    )

    bid_id = db.Column(
        db.Integer,
        db.ForeignKey("bids.id", ondelete="RESTRICT"),
        nullable=False,
        unique=True
    )

    quantity = db.Column(
        db.Numeric(12, 2),
        nullable=False
    )

    price_per_unit = db.Column(
        db.Numeric(12, 2),
        nullable=False
    )

    total_amount = db.Column(
        db.Numeric(14, 2),
        nullable=False
    )

    transaction_date = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    status = db.Column(
        transaction_status,
        nullable=False,
        default="pending"
    )

    completed_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships

    auction = db.relationship(
        "Auction",
        back_populates="transaction"
    )

    listing = db.relationship(
        "ProduceListing",
        back_populates="transaction"
    )

    farmer = db.relationship(
        "FarmerProfile",
        back_populates="transactions"
    )

    buyer = db.relationship(
        "BuyerProfile",
        back_populates="transactions"
    )

    bid = db.relationship(
        "Bid",
        back_populates="transaction"
    )

    payment = db.relationship(
        "Payment",
        back_populates="transaction",
        uselist=False,
        cascade="all, delete-orphan"
    )

    # Relationship

    reviews = db.relationship(
        "RatingReview",
        back_populates="transaction",
        cascade="all, delete-orphan"
    )

    reports = db.relationship(
        "Report",
        back_populates="transaction"
    )

    logistics = db.relationship(
        "Logistics",
        back_populates="transaction",
        uselist=False,
        cascade="all, delete-orphan"
    )