from config import db
from datetime import datetime, timezone
from .enums import logistics_status

class Logistics(db.Model):
    __tablename__ = "logistics"

    id = db.Column(db.Integer, primary_key=True)

    transaction_id = db.Column(
        db.Integer,
        db.ForeignKey("transactions.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    pickup_location = db.Column(
        db.String(255),
        nullable=False
    )

    delivery_location = db.Column(
        db.String(255),
        nullable=False
    )

    distance_km = db.Column(
        db.Numeric(10, 2)
    )

    estimated_transport_cost = db.Column(
        db.Numeric(12, 2)
    )

    estimated_co2 = db.Column(
        db.Numeric(10, 2)
    )

    logistics_status = db.Column(
        logistics_status,
        nullable=False,
        default="pending"
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

    transaction = db.relationship(
        "Transaction",
        back_populates="logistics"
    )