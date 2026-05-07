from models.meta import PageMeta
from extensions import db


def get_meta_by_page(page_id):
    meta = PageMeta.query.filter_by(page_id=page_id).first()

    if not meta:
        raise ValueError("Meta not found")

    return meta


def update_meta(page_id, data):
    meta = PageMeta.query.filter_by(page_id=page_id).first()

    if not meta:
        raise ValueError("Meta not found")

    if "meta_title" in data:
        meta.meta_title = data["meta_title"].strip()

    if "meta_description" in data:
        meta.meta_description = data["meta_description"]

    if "keywords" in data:
        meta.keywords = data["keywords"]

    if "canonical_url" in data:
        meta.canonical_url = data["canonical_url"]

    if "meta_robots" in data:
        meta.meta_robots = data["meta_robots"]

    if "og_graph" in data:
        meta.og_graph = data["og_graph"]  # expects dict

    meta.updated_by ="user_id"

    # Touch parent page
    from models.page import Page
    page = Page.query.get(page_id)
    if page:
        from datetime import datetime
        page.updated_at = datetime.utcnow()

    db.session.commit()

    return meta