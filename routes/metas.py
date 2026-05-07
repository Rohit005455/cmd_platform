from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from services.meta_service import update_meta, get_meta_by_page
from models.page import Page   
from models.meta import PageMeta
meta_bp = Blueprint("meta", __name__)


@meta_bp.route("/meta/<page_id>/edit", methods=["POST"])
def edit_meta(page_id):
    """
    Update SEO and Meta tags for a page
    ---
    parameters:
      - name: page_id
        in: path
        type: string
        required: true
      - name: meta_title
        in: formData
        type: string
      - name: meta_description
        in: formData
        type: string
      - name: og_graph
        in: formData
        type: string
        description: JSON string
    responses:
      302:
        description: Redirects back to page editor
    """
    try:
        data = request.form.to_dict()

        # handle og_graph safely
        if "og_graph" in data and data["og_graph"]:
            import json
            data["og_graph"] = json.loads(data["og_graph"])
        else:
            data["og_graph"] = None

        update_meta(page_id, data)

        page = Page.query.get(page_id)

        if not page:
            return "Page not found", 404

        return redirect(f"/pages/{page.id}")

    except Exception as e:
        return str(e), 400