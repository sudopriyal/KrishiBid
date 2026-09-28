from config import db
from datetime import datetime, timezone
from .enums import listing_status

class ProduceListing(db.Model):
    __tablename__ = "produce_listings"

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

    quantity = db.Column(
        db.Numeric(12, 2),
        nullable=False
    )

    quantity_unit = db.Column(
        db.String(30),
        nullable=False
    )

    quality_grade = db.Column(
        db.String(50),
        nullable=True
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    harvest_date = db.Column(
        db.Date,
        nullable=True
    )

    available_from = db.Column(
        db.DateTime(timezone=True),
        nullable=True
    )

    location = db.Column(
        db.String(255),
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

    starting_price = db.Column(
        db.Numeric(12, 2),
        nullable=False
    )

    status = db.Column(
        listing_status,
        nullable=False,
        default="draft"
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

    # Relationship

    farmer = db.relationship(
        "FarmerProfile",
        back_populates="produce_listings"
    )

    images = db.relationship(
        "ProduceImage",
        back_populates="listing",
        cascade="all, delete-orphan"
    )

    auctions = db.relationship(
        "Auction",
        back_populates="listing",
        cascade="all, delete-orphan"
    )

    transaction = db.relationship(
        "Transaction",
        back_populates="listing",
        uselist=False
    )

    price_insights = db.relationship(
        "PriceInsight",
        back_populates="listing",
        cascade="all, delete-orphan"
    )
    quality_assessments = db.relationship(
        "QualityAssessment",
        back_populates="listing",
        cascade="all, delete-orphan"
    )

    reports = db.relationship(
        "Report",
        back_populates="listing"
    )