from flask import Blueprint, request, render_template, redirect, flash, url_for
from models.page import Page
from models.section import Section
from models.meta import PageMeta

from services.page_service import (
    get_all_pages,
    get_page_with_details,
    update_page,
    create_page,
)

pages_bp = Blueprint("pages", __name__)


# =========================
# 1. LIST ALL PAGES
# =========================
@pages_bp.route("/pages", methods=["GET"])
def list_pages():

    pages = get_all_pages()

    return render_template(
        "page.html",
        pages=pages
    )


# =========================
# 1b. ADD NEW PAGE
# =========================
@pages_bp.route("/pages/add", methods=["POST"])
def create_page_route():
    try:
        data = request.form.to_dict()
        new_page = create_page(data)
        flash("Page created successfully!", "success")
        return redirect(f"/pages/{new_page.id}")
    except ValueError as e:
        flash(str(e), "error")
        return redirect(url_for("pages.list_pages"))


# =========================
# 2. OPEN PAGE EDITOR
# =========================
@pages_bp.route("/pages/<string:page_id>", methods=["GET"])
def edit_page(page_id):

    try:

        data = get_page_with_details(page_id)

        all_pages = get_all_pages()

        return render_template(
            "edit.html",
            page=data["page"],
            sections=data["sections"],
            meta=data["meta"],
            pages=all_pages
        )

    except ValueError as e:
        return str(e), 404


# =========================
# 3. UPDATE PAGE
# =========================
@pages_bp.route("/pages/<string:page_id>/update", methods=["POST"])
def update_page_form(page_id):

    try:

        data = request.form.to_dict()

        page = Page.query.get(page_id)

        if not page:
            return "Page not found", 404

        update_page(page_id, data)

        return redirect(f"/pages/{page_id}")

    except ValueError as e:
        return str(e), 400