from config import db
from datetime import datetime, timezone
from .enums import bid_status

bid_status = db.Enum(
    "active",
    "accepted",
    "rejected",
    "withdrawn",
    name="bid_status"
)


class Bid(db.Model):
    __tablename__ = "bids"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    auction_id = db.Column(
        db.Integer,
        db.ForeignKey("auctions.id", ondelete="CASCADE"),
        nullable=False
    )

    buyer_id = db.Column(
        db.Integer,
        db.ForeignKey("buyer_profiles.id", ondelete="CASCADE"),
        nullable=False
    )

    bid_amount = db.Column(
        db.Numeric(12, 2),
        nullable=False
    )

    bid_time = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    status = db.Column(
        bid_status,
        nullable=False,
        default="active"
    )

    # Relationships

    auction = db.relationship(
        "Auction",
        back_populates="bids"
    )

    buyer = db.relationship(
        "BuyerProfile",
        back_populates="bids"
    )

    transaction = db.relationship(
        "Transaction",
        back_populates="bid",
        uselist=False
    )