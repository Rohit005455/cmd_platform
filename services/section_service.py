import json
from models.section import Section
from extensions import db


def add_section(data):
    section_name = data.get("section_name", "").strip()

    if not section_name:
        raise ValueError("section_name is required")

    # Check if section_name is already taken
    existing = Section.query.filter_by(section_name=section_name).first()
    if existing:
        raise ValueError(f"Section key '{section_name}' is already taken")

    # convert comma-separated → list
    image_urls = data.get("image_urls")
    video_urls = data.get("video_urls")

    image_list = [i.strip() for i in image_urls.split(",")] if image_urls else []
    video_list = [v.strip() for v in video_urls.split(",")] if video_urls else []

    section = Section(
        page_id=data.get("page_id"),
        type=data.get("type", "custom"),

        section_name=section_name,

        name=data.get("name"),
        description=data.get("description"),
        html_content=data.get("html_content"),

        image_urls=image_list if image_list else None,
        video_urls=video_list if video_list else None,

        order_index=int(data.get("order_index", 0)),
        is_active=True if data.get("is_active") else False,

        created_by="user-1",
        updated_by="user-1"
    )

    db.session.add(section)
    
    # Touch parent page
    from models.page import Page
    page = Page.query.get(data.get("page_id"))
    if page:
        from datetime import datetime
        page.updated_at = datetime.utcnow()
    
    db.session.commit()

    return section

def update_section(section_id, data):
    section = Section.query.get(section_id)

    if not section:
        raise ValueError("Section not found")

    # section_name update
    if "section_name" in data:
        section_name = data["section_name"].strip()

        if not section_name:
            raise ValueError("section_name cannot be empty")

        # Check if another section already uses this key
        existing = Section.query.filter(
            Section.section_name == section_name,
            Section.id != section_id          # exclude current section
        ).first()

        if existing:
            raise ValueError(f"Section key '{section_name}' is already taken")

        section.section_name = section_name

    if "type" in data:
        section.type = data["type"]

    if "name" in data:
        section.name = data["name"]

    if "description" in data:
        section.description = data["description"]

    if "html_content" in data:
        section.html_content = data["html_content"]

    # convert comma-separated → list
    if "image_urls" in data:
        image_urls = data.get("image_urls")
        section.image_urls = [i.strip() for i in image_urls.split(",")] if image_urls else None

    if "video_urls" in data:
        video_urls = data.get("video_urls")
        section.video_urls = [v.strip() for v in video_urls.split(",")] if video_urls else None

    if "order_index" in data:
        section.order_index = int(data.get("order_index", 0))

    section.is_active = True if data.get("is_active") else False

    section.updated_by = "user-1"

    # Touch parent page
    from models.page import Page
    page = Page.query.get(section.page_id)
    if page:
        from datetime import datetime
        page.updated_at = datetime.utcnow()

    db.session.commit()

    return section