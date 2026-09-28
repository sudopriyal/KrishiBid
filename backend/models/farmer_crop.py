from config import db
from datetime import datetime, timezone


class FarmerCrop(db.Model):
    __tablename__ = "farmer_crops"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    farmer_id = db.Column(
        db.Integer,
        db.ForeignKey("farmer_profiles.id", ondelete="CASCADE"),
        nullable=False
    )

    crop_name = db.Column(
        db.String(100),
        nullable=False
    )

    crop_type = db.Column(
        db.String(100),
        nullable=True
    )

    season = db.Column(
        db.String(50),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationship

    farmer = db.relationship(
        "FarmerProfile",
        back_populates="crops"
    )