from config import db
from datetime import datetime, timezone


class RatingReview(db.Model):
    __tablename__ = "ratings_reviews"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    transaction_id = db.Column(
        db.Integer,
        db.ForeignKey("transactions.id", ondelete="CASCADE"),
        nullable=False
    )

    reviewer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    reviewee_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    rating = db.Column(
        db.Numeric(2, 1),
        nullable=False
    )

    review = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships

    transaction = db.relationship(
        "Transaction",
        back_populates="reviews"
    )

    reviewer = db.relationship(
        "User",
        foreign_keys=[reviewer_id],
        back_populates="reviews_given"
    )

    reviewee = db.relationship(
        "User",
        foreign_keys=[reviewee_id],
        back_populates="reviews_received"
    )