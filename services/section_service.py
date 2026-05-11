import json
from sqlalchemy.orm.attributes import flag_modified
from models.section import Section
from extensions import db




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

    # Isolated update logic based on section type
    current_content = section.content or {}

    if section.type == "hero":
        if "hero_banner" in data:
            current_content["hero_banner"] = data["hero_banner"]
        if "hero_heading" in data:
            current_content["hero_heading"] = data["hero_heading"]
        if "hero_subheading" in data:
            current_content["hero_subheading"] = data["hero_subheading"]
    
    elif section.type == "milestone":
        if "cars_count" in data:
            current_content["cars_count"] = data["cars_count"]
        if "years_count" in data:
            current_content["years_count"] = data["years_count"]
        if "customers_count" in data:
            current_content["customers_count"] = data["customers_count"]
        if "rating" in data:
            current_content["rating"] = data["rating"]
    
    elif section.type == "franchise":
        if "franchise_count" in data:
            current_content["franchise_count"] = data["franchise_count"]
        if "franchise_locations" in data:
            current_content["franchise_locations"] = data["franchise_locations"]
    
    elif section.type == "testimonial":
        # Handle as JSON string if passed as 'items'
        if "items" in data:
            try:
                import json
                current_content["items"] = json.loads(data["items"]) if isinstance(data["items"], str) else data["items"]
            except:
                pass
    
    elif section.type == "faq":
        # Handle as JSON string if passed as 'items'
        if "items" in data:
            try:
                import json
                current_content["items"] = json.loads(data["items"]) if isinstance(data["items"], str) else data["items"]
            except:
                pass
    
    section.content = current_content
    flag_modified(section, "content")

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
