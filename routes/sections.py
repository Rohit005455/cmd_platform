from flask import Blueprint, request, redirect, url_for, flash
from services.section_service import add_section, update_section
from models.page import Page
from models.section import Section

sections_bp = Blueprint("sections", __name__)


# ADD SECTION
@sections_bp.route("/sections/add", methods=["POST"])
def create_section():
    """
    Add a new content section to a page
    ---
    parameters:
      - name: page_id
        in: formData
        type: string
        required: true
      - name: section_name
        in: formData
        type: string
        required: true
      - name: type
        in: formData
        type: string
      - name: name
        in: formData
        type: string
    responses:
      302:
        description: Redirects back to page editor
    """
    data = request.form.to_dict()
    page_id = data.get("page_id")
    
    try:
        section = add_section(data)
        flash("Section added successfully!", "success")
    except ValueError as e:
        flash(str(e), "error")
        return redirect(f"/pages/{page_id}")

    return redirect(f"/pages/{page_id}")


# EDIT SECTION
@sections_bp.route("/sections/<string:section_id>/edit", methods=["POST"])
def edit_section(section_id):
    """
    Update an existing content section
    ---
    parameters:
      - name: section_id
        in: path
        type: string
        required: true
      - name: name
        in: formData
        type: string
      - name: html_content
        in: formData
        type: string
      - name: is_active
        in: formData
        type: boolean
    responses:
      302:
        description: Redirects back to page editor
    """
    data = request.form.to_dict()

    section = Section.query.filter_by(id=section_id).first()
    if not section:
        flash("Section not found", "error")
        return redirect("/pages")

    try:
        update_section(section.id, data)
        flash("Section updated successfully!", "success")
    except ValueError as e:
        flash(str(e), "error")
    
    return redirect(f"/pages/{section.page_id}")