from extensions import db
import uuid
from datetime import datetime

class Page(db.Model):
    __tablename__ = "pages"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(255), nullable=False)  
    slug = db.Column(db.String(255), unique=True, nullable=False)
    misc_data = db.Column(db.Text)

    created_by = db.Column(db.String(36), nullable=False)
    updated_by = db.Column(db.String(36), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)