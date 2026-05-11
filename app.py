from flask import Flask, redirect, url_for
from flasgger import Swagger
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
swagger = Swagger(app)

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

    # Seed Home page if it doesn't exist
    if not Page.query.filter_by(slug="home").first():
        page = Page(
            title="Home",
            slug="home",
            created_by="user-1",
            updated_by="user-1"
        )
        db.session.add(page)
        db.session.flush()  # get page.id

        # Add Hero Section
        hero = Section(
            page_id=page.id,
            type="hero",
            section_name="hero_main",
            name="Main Hero",
            description="The main hero banner for the homepage",
            content={
                "hero_banner": "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?auto=format&fit=crop&q=80&w=2832",
                "hero_heading": "The Future of Digital Content",
                "hero_subheading": "Experience the world's most advanced headless CMS platform with ContentOS."
            },
            order_index=0,
            is_active=True,
            updated_by="user-1"
        )
        db.session.add(hero)

        # Add Milestone Section
        milestones = Section(
            page_id=page.id,
            type="milestone",
            section_name="milestones_main",
            name="Key Milestones",
            description="Company achievements and statistics",
            content={
                "cars_count": "500+",
                "years_count": "15",
                "customers_count": "2000+",
                "rating": "4.9/5"
            },
            order_index=1,
            is_active=True,
            updated_by="user-1"
        )
        db.session.add(milestones)

        # Add Franchise Section
        franchise = Section(
            page_id=page.id,
            type="franchise",
            section_name="franchise_main",
            name="Franchise Network",
            description="Our growing network of franchise partners",
            content={
                "franchise_count": "50+",
                "franchise_locations": "Mumbai, Delhi, Bangalore, Pune, Hyderabad"
            },
            order_index=2,
            is_active=True,
            updated_by="user-1"
        )
        db.session.add(franchise)

        meta = PageMeta(
            page_id=page.id,
            meta_title="Home | ContentOS",
            updated_by="user-1"
        )
        db.session.add(meta)
        db.session.commit()

    # Ensure Home Page has Testimonial and FAQ sections
    home_page = Page.query.filter_by(slug="home").first()
    if home_page:
        # Testimonials
        if not Section.query.filter_by(page_id=home_page.id, section_name="testimonials_home").first():
            testimonials = Section(
                page_id=home_page.id,
                type="testimonial",
                section_name="testimonials_home",
                name="Customer Testimonials",
                description="What our clients say about us",
                content={
                    "items": [
                        {"name": "John Doe", "role": "CEO, TechCorp", "quote": "ContentOS has transformed our workflow.", "avatar": "https://i.pravatar.cc/150?u=1"},
                        {"name": "Jane Smith", "role": "Product Manager", "quote": "The best CMS I've ever used.", "avatar": "https://i.pravatar.cc/150?u=2"}
                    ]
                },
                order_index=3,
                is_active=True,
                updated_by="user-1"
            )
            db.session.add(testimonials)

        # FAQ
        if not Section.query.filter_by(page_id=home_page.id, section_name="faq_home").first():
            faq = Section(
                page_id=home_page.id,
                type="faq",
                section_name="faq_home",
                name="Frequently Asked Questions",
                description="Common questions about our services",
                content={
                    "items": [
                        {"question": "Is it secure?", "answer": "Yes, we use enterprise-grade security."},
                        {"question": "How do I get started?", "answer": "Simply sign up and create your first page."}
                    ]
                },
                order_index=4,
                is_active=True,
                updated_by="user-1"
            )
            db.session.add(faq)
        
        db.session.commit()

    # Seed About page if it doesn't exist
    if not Page.query.filter_by(slug="about").first():
        about_page = Page(
            title="About Us",
            slug="about",
            created_by="user-1",
            updated_by="user-1"
        )
        db.session.add(about_page)
        db.session.flush()

        # Hero for About
        about_hero = Section(
            page_id=about_page.id,
            type="hero",
            section_name="about_hero",
            name="About Hero",
            description="Introduction to our company",
            content={
                "hero_banner": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&q=80&w=2832",
                "hero_heading": "Our Story",
                "hero_subheading": "We are building the future of content management, one block at a time."
            },
            order_index=0,
            is_active=True,
            updated_by="user-1"
        )
        db.session.add(about_hero)

        # Meta for About
        about_meta = PageMeta(
            page_id=about_page.id,
            meta_title="About Us | ContentOS",
            updated_by="user-1"
        )
        db.session.add(about_meta)
        db.session.commit()


@app.route("/")
def home():
    page = Page.query.filter_by(slug="home").first()
    if page:
        return redirect(url_for("pages.edit_page", page_id=page.id))
    return redirect(url_for("pages.list_pages"))


if __name__ == "__main__":
    app.run(debug=True)