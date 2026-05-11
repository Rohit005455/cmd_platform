import sys
import os

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models.page import Page
with app.app_context():
    pages = Page.query.all()
    for p in pages:
        print(f"ID: {p.id}, Title: {p.title}")
