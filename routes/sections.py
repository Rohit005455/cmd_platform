import os
from flask import Blueprint, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from services.section_service import update_section
from models.page import Page
from models.section import Section

sections_bp = Blueprint("sections", __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

# EDIT SECTION
@sections_bp.route("/sections/<string:section_id>/edit", methods=["POST"])
def edit_section(section_id):
    data = request.form.to_dict()

    section = Section.query.filter_by(id=section_id).first()
    if not section:
        flash("Section not found", "error")
        return redirect("/")

    # Handle file upload
    if 'hero_banner_file' in request.files:
        file = request.files['hero_banner_file']
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Add timestamp to filename to avoid collisions
            from datetime import datetime
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
            
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            # ensure directory exists
            os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(upload_path)
            
            # Store the relative path in the database
            data['hero_banner'] = f"/{upload_path}"

    try:
        update_section(section.id, data)
        flash("Section updated successfully!", "success")
    except ValueError as e:
        flash(str(e), "error")
    
    return redirect(f"/pages/{section.page_id}")
