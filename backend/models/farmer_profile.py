from config import db
from datetime import datetime, timezone


class FarmerProfile(db.Model):
    __tablename__ = "farmer_profiles"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    farm_name = db.Column(
        db.String(150),
        nullable=True
    )

    farm_location = db.Column(
        db.String(255),
        nullable=True
    )

    district = db.Column(
        db.String(100),
        nullable=True
    )

    state = db.Column(
        db.String(100),
        nullable=True
    )

    latitude = db.Column(
        db.Numeric(10, 7),
        nullable=True
    )

    longitude = db.Column(
        db.Numeric(10, 7),
        nullable=True
    )

    farm_size = db.Column(
        db.Numeric(10, 2),
        nullable=True
    )

    farm_size_unit = db.Column(
        db.String(20),
        nullable=True
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

    # Relationships

    user = db.relationship(
        "User",
        back_populates="farmer_profile"
    )

    crops = db.relationship(
        "FarmerCrop",
        back_populates="farmer",
        cascade="all, delete-orphan"
    )

    produce_listings = db.relationship(
        "ProduceListing",
        back_populates="farmer",
        cascade="all, delete-orphan"
    )

    transactions = db.relationship(
        "Transaction",
        back_populates="farmer"
    )