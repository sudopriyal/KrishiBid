from config import db
from datetime import datetime, timezone


class ProduceImage(db.Model):
    __tablename__ = "produce_images"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    listing_id = db.Column(
        db.Integer,
        db.ForeignKey("produce_listings.id", ondelete="CASCADE"),
        nullable=False
    )

    image_url = db.Column(
        db.String(500),
        nullable=False
    )

    is_primary = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    uploaded_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationship

    listing = db.relationship(
        "ProduceListing",
        back_populates="images"
    )

    quality_assessments = db.relationship(
        "QualityAssessment",
        back_populates="image",
        cascade="all, delete-orphan"
    )