from config import db
from datetime import datetime, timezone
from .enums import report_type, report_status

class Report(db.Model):
    __tablename__ = "reports"

    id = db.Column(db.Integer, primary_key=True)

    reported_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    reported_user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )

    listing_id = db.Column(
        db.Integer,
        db.ForeignKey("produce_listings.id", ondelete="SET NULL"),
        nullable=True
    )

    transaction_id = db.Column(
        db.Integer,
        db.ForeignKey("transactions.id", ondelete="SET NULL"),
        nullable=True
    )

    report_type = db.Column(
        report_type,
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    status = db.Column(
        report_status,
        nullable=False,
        default="pending"
    )

    admin_notes = db.Column(db.Text)

    resolved_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )

    resolved_at = db.Column(db.DateTime(timezone=True))

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    reporter = db.relationship(
        "User",
        foreign_keys=[reported_by],
        back_populates="reports_filed"
    )

    reported_user = db.relationship(
        "User",
        foreign_keys=[reported_user_id],
        back_populates="reports_received"
    )

    resolver = db.relationship(
        "User",
        foreign_keys=[resolved_by],
        back_populates="reports_resolved"
    )

    listing = db.relationship(
        "ProduceListing",
        back_populates="reports"
    )

    transaction = db.relationship(
        "Transaction",
        back_populates="reports"
    )