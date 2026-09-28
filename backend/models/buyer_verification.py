from config import db
from datetime import datetime, timezone
from .enums import verification_status

class BuyerVerification(db.Model):
    __tablename__ = "buyer_verifications"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    buyer_id = db.Column(
        db.Integer,
        db.ForeignKey("buyer_profiles.id", ondelete="CASCADE"),
        nullable=False
    )

    document_type = db.Column(
        db.String(50),
        nullable=False
    )

    document_number = db.Column(
        db.String(100),
        nullable=False
    )

    document_url = db.Column(
        db.String(500),
        nullable=True
    )

    verification_status = db.Column(
        verification_status,
        nullable=False,
        default="pending"
    )

    verified_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )

    verified_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True
    )

    rejection_reason = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships

    buyer = db.relationship(
        "BuyerProfile",
        back_populates="verifications"
    )

    verifier = db.relationship(
        "User",
        back_populates="buyer_verifications"
    )