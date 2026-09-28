from config import db

# buyer_profile.py
verification_status = db.Enum(
    "pending",
    "approved",
    "rejected",
    name="verification_status"
)

# auction.py
auction_status = db.Enum(
    "scheduled",
    "active",
    "ended",
    "cancelled",
    name="auction_status"
)

# bid.py
bid_status = db.Enum(
    "active",
    "accepted",
    "rejected",
    "withdrawn",
    name="bid_status"
)

# logistics.py
logistics_status = db.Enum(
    "pending",
    "assigned",
    "in_transit",
    "delivered",
    "cancelled",
    name="logistics_status"
)

# notification.py
notification_type = db.Enum(
    "bid",
    "auction",
    "transaction",
    "payment",
    "verification",
    "listing",
    "system",
    name="notification_type"
)

# payment.py
payment_method = db.Enum(
    "mock",
    "upi",
    "card",
    "bank_transfer",
    name="payment_method"
)

payment_status = db.Enum(
    "pending",
    "paid",
    "failed",
    "refunded",
    name="payment_status"
)

# produce_listing.py
listing_status = db.Enum(
    "draft",
    "active",
    "sold",
    "expired",
    "cancelled",
    name="listing_status"
)

# report.py
report_type = db.Enum(
    "fraud",
    "misconduct",
    "fake_listing",
    "payment_issue",
    "quality_issue",
    "other",
    name="report_type"
)

report_status = db.Enum(
    "pending",
    "investigating",
    "resolved",
    "rejected",
    name="report_status"
)

# transaction.py
transaction_status = db.Enum(
    "pending",
    "confirmed",
    "completed",
    "cancelled",
    name="transaction_status"
)

# user.py
user_role = db.Enum(
    "farmer",
    "buyer",
    "admin",
    name="user_role"
)

user_status = db.Enum(
    "active",
    "inactive",
    "suspended",
    "pending",
    name="user_status"
)