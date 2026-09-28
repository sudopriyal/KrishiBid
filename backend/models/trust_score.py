from config import db
from datetime import datetime, timezone


class TrustScore(db.Model):
    __tablename__ = "trust_scores"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    trust_score = db.Column(
        db.Numeric(5, 2),
        nullable=False,
        default=0
    )

    completed_transactions = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    cancelled_transactions = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    total_ratings = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    average_rating = db.Column(
        db.Numeric(3, 2),
        nullable=True
    )

    last_calculated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationship

    user = db.relationship(
        "User",
        back_populates="trust_score"
    )