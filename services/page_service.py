from models.page import Page
from models.section import Section
from models.meta import PageMeta
from extensions import db
from utils.validators import validate_update_page

def get_page_with_details_by_slug(slug):
    page = Page.query.filter_by(slug=slug).first()

    if not page:
        raise ValueError("Page not found")

    sections = page.sections
    meta = PageMeta.query.filter_by(page_id=page.id).first()

    return {
        "page": page,
        "sections": sections,
        "meta": meta
    }

def get_all_pages():
    return Page.query.all()


def get_page_with_details(page_id):
    page = Page.query.get(page_id)

    if not page:
        raise ValueError("Page not found")

    sections = Section.query.filter_by(page_id=page_id)\
        .order_by(Section.order_index).all()

    meta = PageMeta.query.filter_by(page_id=page_id).first()

    return {
        "page": page,
        "sections": sections,
        "meta": meta
    }

def update_page(page_id, data):

    page = Page.query.get(page_id)

    if not page:
        raise ValueError("Page not found")

    validate_update_page(data)

    # UPDATE TITLE
    if "title" in data and data["title"]:
        page.title = data["title"].strip()

    # UPDATE SLUG
    if "slug" in data and data["slug"]:

        new_slug = data["slug"].strip().lower()

        # remove spaces
        new_slug = new_slug.replace(" ", "-")

        # check duplicate slug
        existing_page = Page.query.filter(
            Page.slug == new_slug,
            Page.id != page.id
        ).first()

        if existing_page:
            raise ValueError("Slug already exists")
  
        page.slug = new_slug

    # UPDATE MISC DATA
    if "misc_data" in data:
        page.misc_data = data["misc_data"]

    page.updated_by = "user_1"

    db.session.commit()

    return page

def create_page(data):
    title = data.get("title", "").strip()
    slug = data.get("slug", "").strip().lower()
    misc_data = data.get("misc_data", "")

    if not title:
        raise ValueError("Title is required")
    if not slug:
        raise ValueError("Slug is required")

    # remove spaces from slug
    slug = slug.replace(" ", "-")

    # check duplicate slug
    existing_page = Page.query.filter_by(slug=slug).first()
    if existing_page:
        raise ValueError("Slug already exists")

    page = Page(
        title=title,
        slug=slug,
        misc_data=misc_data,
        created_by="user-1",
        updated_by="user-1"
    )
    db.session.add(page)
    db.session.flush()

    # Create default meta for the new page
    meta = PageMeta(
        page_id=page.id,
        meta_title=title,
        updated_by="user-1"
    )
    db.session.add(meta)
    
    db.session.commit()
    return page
def generate_slug(title):
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    return slug