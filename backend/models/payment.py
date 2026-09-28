from config import db
from datetime import datetime, timezone
from .enums import payment_method, payment_status

class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    transaction_id = db.Column(
        db.Integer,
        db.ForeignKey("transactions.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    amount = db.Column(
        db.Numeric(14, 2),
        nullable=False
    )

    payment_method = db.Column(
        payment_method,
        nullable=False,
        default="mock"
    )

    payment_reference = db.Column(
        db.String(255),
        nullable=True
    )

    payment_status = db.Column(
        payment_status,
        nullable=False,
        default="pending"
    )

    paid_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationship

    transaction = db.relationship(
        "Transaction",
        back_populates="payment"
    )