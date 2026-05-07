from flask import Flask, redirect, url_for
from config import Config
from extensions import db

# import blueprints
from routes.pages import pages_bp
from routes.sections import sections_bp
from routes.metas import meta_bp

# 🔥 IMPORT ALL MODELS (IMPORTANT)
from models.page import Page
from models.meta import PageMeta
from models.section import Section
from datetime import datetime, timedelta

app = Flask(__name__)
app.config.from_object(Config)

# IST Timezone Filter
@app.template_filter('ist')
def convert_to_ist(utc_dt):
    if not utc_dt:
        return None
    return utc_dt + timedelta(hours=5, minutes=30)

db.init_app(app)

app.register_blueprint(pages_bp)
app.register_blueprint(sections_bp)
app.register_blueprint(meta_bp)


with app.app_context():
    db.create_all()   # ✅ make sure tables + relationships are created

    # seed data only if empty
    if not Page.query.first():

        pages_data = [
            {"title": "Home", "slug": "home"},
            {"title": "About", "slug": "about"},
            {"title": "Services", "slug": "services"},
            {"title": "Contact", "slug": "contact"},
        ]

        for p in pages_data:
            page = Page(
                title=p["title"],
                slug=p["slug"],
                created_by="user-1",
                updated_by="user-1"
            )
            db.session.add(page)
            db.session.flush()  # get page.id

            meta = PageMeta(
                page_id=page.id,
                meta_title=p["title"],
                updated_by="user-1"
            )
            db.session.add(meta)

        db.session.commit()


@app.route("/")
def home():
    return redirect(url_for("pages.list_pages"))


if __name__ == "__main__":
    app.run(debug=True)