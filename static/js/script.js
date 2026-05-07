/* ============================================
   ContentOS CMS – script.js
   ============================================ */

/**
 * Toggles the mobile sidebar and overlay
 */
function toggleMobileSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    if (sidebar && overlay) {
        sidebar.classList.toggle('open');
        overlay.classList.toggle('active');
    }
}

/**
 * Toggles a section edit form
 */
function toggleSection(id) {
    const el = document.getElementById('edit-' + id);
    const chev = document.getElementById('chev-' + id);
    if (el) {
        const isOpen = el.classList.toggle('open');
        if (chev) {
            chev.style.transform = isOpen ? 'rotate(180deg)' : 'rotate(0deg)';
        }
    }
}

/**
 * Toggles the SEO/Meta edit form
 */
function toggleMeta() {
    const form = document.getElementById('meta-form');
    const prev = document.getElementById('meta-preview');
    const btn = document.getElementById('meta-toggle-btn');
    if (form && prev && btn) {
        const isOpen = form.classList.toggle('open');
        prev.style.display = isOpen ? 'none' : 'block';
        btn.textContent = isOpen ? 'Cancel' : 'Edit';
        btn.classList.toggle('btn-primary', isOpen);
    }
}

/**
 * Toggles the add section form
 */
function toggleAddSection() {
    const el = document.getElementById('add-section-form');
    if (el) el.classList.toggle('open');
}

/**
 * Filters the pages list based on search input
 */
function filterPages(query) {
    const items = document.querySelectorAll('#pages-list .page-row');
    const noResults = document.getElementById('no-results');
    const countBadge = document.getElementById('visible-count');
    const q = query.trim().toLowerCase();
    let visible = 0;

    items.forEach(function(item) {
        const match = (item.getAttribute('data-title') || '').indexOf(q) !== -1;
        item.style.display = match ? 'flex' : 'none';
        if (match) visible++;
    });

    if (noResults) noResults.style.display = visible === 0 ? 'flex' : 'none';
    if (countBadge) countBadge.textContent = visible + ' active';
}

/**
 * Toggles the add page form
 */
function toggleAddPage() {
    const el = document.getElementById('add-page-form');
    if (el) el.classList.toggle('open');
}

/**
 * Filters the sections list in the edit page
 */
function filterSections() {
    const input = document.getElementById('section-search');
    if (!input) return;
    
    const q = input.value.trim().toLowerCase();
    const items = document.querySelectorAll('.sections-list .section-item');
    
    items.forEach(function(item) {
        const name = (item.querySelector('.section-name')?.textContent || '').toLowerCase();
        const meta = (item.querySelector('.section-meta')?.textContent || '').toLowerCase();
        const match = name.includes(q) || meta.includes(q);
        item.style.display = match ? 'block' : 'none';
    });
}



