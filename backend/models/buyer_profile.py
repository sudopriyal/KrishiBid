from config import db
from datetime import datetime, timezone
from .enums import verification_status


class BuyerProfile(db.Model):
    __tablename__ = "buyer_profiles"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    business_name = db.Column(
        db.String(150),
        nullable=True
    )

    business_type = db.Column(
        db.String(100),
        nullable=True
    )

    business_description = db.Column(
        db.Text,
        nullable=True
    )

    business_address = db.Column(
        db.String(255),
        nullable=True
    )

    district = db.Column(
        db.String(100),
        nullable=True
    )

    state = db.Column(
        db.String(100),
        nullable=True
    )

    latitude = db.Column(
        db.Numeric(10, 7),
        nullable=True
    )

    longitude = db.Column(
        db.Numeric(10, 7),
        nullable=True
    )

    verification_status = db.Column(
        verification_status,
        nullable=False,
        default="pending"
    )

    verification_document = db.Column(
        db.String(255),
        nullable=True
    )

    verified_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships

    user = db.relationship(
        "User",
        back_populates="buyer_profile"
    )

    preferences = db.relationship(
        "BuyerPreference",
        back_populates="buyer",
        cascade="all, delete-orphan"
    )

    won_auctions = db.relationship(
        "Auction",
        back_populates="highest_bidder"
    )

    bids = db.relationship(
        "Bid",
        back_populates="buyer",
        cascade="all, delete-orphan"
    )

    transactions = db.relationship(
        "Transaction",
        back_populates="buyer"
    )

    verifications = db.relationship(
        "BuyerVerification",
        back_populates="buyer",
        cascade="all, delete-orphan"
    )