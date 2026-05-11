import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models.page import Page
from models.section import Section

with app.app_context():
    page = Page.query.filter_by(slug="home").first()
    if page:
        print(f"Page: {page.title}")
        print("Sections:")
        for s in page.sections:
            print(f"- {s.name} (Type: {s.type}, Key: {s.section_name})")
    else:
        print("Home page not found")
