from config import db
from datetime import datetime, timezone


class BuyerPreference(db.Model):
    __tablename__ = "buyer_preferences"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    buyer_id = db.Column(
        db.Integer,
        db.ForeignKey("buyer_profiles.id", ondelete="CASCADE"),
        nullable=False
    )

    crop_name = db.Column(
        db.String(100),
        nullable=False
    )

    preferred_quality = db.Column(
        db.String(50),
        nullable=True
    )

    minimum_quantity = db.Column(
        db.Numeric(12, 2),
        nullable=True
    )

    maximum_quantity = db.Column(
        db.Numeric(12, 2),
        nullable=True
    )

    preferred_location = db.Column(
        db.String(255),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationship

    buyer = db.relationship(
        "BuyerProfile",
        back_populates="preferences"
    )