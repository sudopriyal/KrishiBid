from config import db
from datetime import datetime, timezone


class QualityAssessment(db.Model):
    __tablename__ = "quality_assessments"

    id = db.Column(db.Integer, primary_key=True)

    listing_id = db.Column(
        db.Integer,
        db.ForeignKey("produce_listings.id", ondelete="CASCADE"),
        nullable=False
    )

    image_id = db.Column(
        db.Integer,
        db.ForeignKey("produce_images.id", ondelete="CASCADE"),
        nullable=False
    )

    predicted_grade = db.Column(db.String(50))

    quality_score = db.Column(db.Numeric(5, 2))
    confidence_score = db.Column(db.Numeric(5, 4))

    detected_defects = db.Column(db.JSON)

    model_version = db.Column(db.String(50))

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    listing = db.relationship(
        "ProduceListing",
        back_populates="quality_assessments"
    )

    image = db.relationship(
        "ProduceImage",
        back_populates="quality_assessments"
    )