from config import db
from datetime import datetime, timezone
from .enums import user_role, user_status

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    phone = db.Column(db.String(20))

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        user_role,
        nullable=False
    )

    status = db.Column(
        user_status,
        nullable=False,
        default="active"
    )

    profile_image = db.Column(db.String(255))

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

    farmer_profile = db.relationship(
        "FarmerProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    buyer_profile = db.relationship(
        "BuyerProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    buyer_verifications = db.relationship(
        "BuyerVerification",
        back_populates="verifier"
    )

    trust_score = db.relationship(
        "TrustScore",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    
    reviews_given = db.relationship(
        "RatingReview",
        foreign_keys="RatingReview.reviewer_id",
        back_populates="reviewer",
        cascade="all, delete-orphan"
    )
    
    reviews_received = db.relationship(
        "RatingReview",
        foreign_keys="RatingReview.reviewee_id",
        back_populates="reviewee",
        cascade="all, delete-orphan"
    )

    notifications = db.relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    reports_filed = db.relationship(
        "Report",
        foreign_keys="Report.reported_by",
        back_populates="reporter",
        cascade="all, delete-orphan"
    )
    
    reports_received = db.relationship(
        "Report",
        foreign_keys="Report.reported_user_id",
        back_populates="reported_user"
    )
    
    reports_resolved = db.relationship(
        "Report",
        foreign_keys="Report.resolved_by",
        back_populates="resolver"
    )