from extensions import db
import uuid
from datetime import datetime

class Section(db.Model):
    __tablename__ = "sections"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    page_id = db.Column(db.String(36), db.ForeignKey("pages.id"), nullable=False)

    type = db.Column(db.String(50), nullable=False)

    section_name = db.Column(db.String(255), nullable=False, unique=True)  
    name = db.Column(db.String(255), nullable=False)

    description = db.Column(db.Text, nullable=True)
    html_content = db.Column(db.Text, nullable=True)

    image_urls = db.Column(db.JSON, nullable=True)
    video_urls = db.Column(db.JSON, nullable=True)

    order_index = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    created_by = db.Column(db.String(36), nullable=False)
    updated_by = db.Column(db.String(36), nullable=False)
    page = db.relationship("Page", backref=db.backref("sections", lazy=True))