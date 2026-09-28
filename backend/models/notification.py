from config import db
from datetime import datetime, timezone
from .enums import notification_type

class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)

    notification_type = db.Column(
        notification_type,
        nullable=False
    )

    reference_type = db.Column(db.String(50))
    reference_id = db.Column(db.Integer)

    is_read = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    user = db.relationship(
        "User",
        back_populates="notifications"
    )