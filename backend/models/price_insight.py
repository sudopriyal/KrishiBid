from config import db
from datetime import datetime, timezone


class PriceInsight(db.Model):
    __tablename__ = "price_insights"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    listing_id = db.Column(
        db.Integer,
        db.ForeignKey("produce_listings.id", ondelete="CASCADE"),
        nullable=False
    )

    estimated_min_price = db.Column(
        db.Numeric(12, 2),
        nullable=False
    )

    estimated_max_price = db.Column(
        db.Numeric(12, 2),
        nullable=False
    )

    estimated_average_price = db.Column(
        db.Numeric(12, 2),
        nullable=False
    )

    current_market_price = db.Column(
        db.Numeric(12, 2),
        nullable=True
    )

    model_version = db.Column(
        db.String(50),
        nullable=True
    )

    confidence_score = db.Column(
        db.Numeric(5, 4),
        nullable=True
    )

    generated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationship

    listing = db.relationship(
        "ProduceListing",
        back_populates="price_insights"
    )