from extensions import db
import uuid
from datetime import datetime


class PageMeta(db.Model):
    __tablename__ = "page_meta"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    page_id = db.Column(
        db.String(36),
        db.ForeignKey("pages.id"),
        unique=True,
        nullable=False
    )

    meta_title = db.Column(db.String(60), nullable=False)
    meta_description = db.Column(db.String(160))
    keywords = db.Column(db.String(500))
    canonical_url = db.Column(db.String(2048))

    meta_robots = db.Column(db.String(20), default="index,follow")

    og_graph = db.Column(db.JSON)

    # ✅ audit fields (only update tracking)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    updated_by = db.Column(db.String(36), nullable=False)