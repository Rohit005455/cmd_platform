import re
import json
from models.page import Page
from models.section import Section
def validate_update_page(data):
    errors = {}

    if "title" in data:
        title = data["title"].strip()
        if not title:
            errors["title"] = "Title cannot be empty"

        elif len(title) < 3 or len(title) > 255:
            errors["title"] = "Must be between 3 and 255 characters"

        elif "<" in title or ">" in title:
            errors["title"] = "HTML not allowed"

    if "slug" in data:
        slug = data["slug"].strip()

        if not slug:
            errors["slug"] = "Slug cannot be empty"

        elif not re.match(r"^[a-z0-9-]+$", slug):
            errors["slug"] = "Only lowercase letters, numbers, hyphens allowed"

        elif "--" in slug:
            errors["slug"] = "Slug cannot contain consecutive hyphens"

    if "misc_data" in data:
        misc = data["misc_data"]

        if misc:
            if len(misc) > 5000:
                errors["misc_data"] = "Too large (max 5000 chars)"

            # try:
            #     json.loads(misc)
            # except:
            #     errors["misc_data"] = "Must be valid JSON"

    if errors:
        raise ValueError(errors)



ALLOWED_ROBOTS = {
    "index,follow",
    "noindex,follow",
    "index,nofollow",
    "noindex,nofollow"
}


def validate_update_meta(data):
    errors = {}

    # META TITLE
    if "meta_title" in data:
        title = data["meta_title"].strip()

        if not title:
            errors["meta_title"] = "Meta title cannot be empty"

        elif len(title) > 60:
            errors["meta_title"] = "Max 60 characters"

    # META DESCRIPTION
    if "meta_description" in data:
        desc = data["meta_description"].strip()

        if len(desc) > 160:
            errors["meta_description"] = "Max 160 characters"

    # KEYWORDS
    if "keywords" in data:
        keywords = data["keywords"].strip()

        if len(keywords) > 500:
            errors["keywords"] = "Max 500 characters"

    # CANONICAL URL
    if "canonical_url" in data:
        url = data["canonical_url"].strip()

        if url and not re.match(r"^https?://", url):
            errors["canonical_url"] = "Must be a valid URL (http/https)"

    # META ROBOTS
    if "meta_robots" in data:
        if data["meta_robots"] not in ALLOWED_ROBOTS:
            errors["meta_robots"] = "Invalid robots value"

    # OG GRAPH (only type check)
    if "og_graph" in data:
        og = data["og_graph"]

        if og is not None and not isinstance(og, dict):
            errors["og_graph"] = "Must be a valid JSON object"

    if errors:
        raise ValueError(errors)

def validate_section(data, section_id=None):
    errors = {}

    section_name = data.get("section_name", "").strip()

    if not section_name:
        errors["section_name"] = "Section name is required"

    elif not re.match(r"^[a-z0-9_-]+$", section_name):
        errors["section_name"] = "Only lowercase, numbers, _ and - allowed"

    else:
        existing = Section.query.filter_by(section_name=section_name).first()

        if existing and existing.id != section_id:
            errors["section_name"] = "Must be unique"

    if errors:
        raise ValueError(errors)