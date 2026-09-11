"""Merge the cover and body PDFs rendered by render.js into the final deliverable."""
import os
import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cover = os.path.join(ROOT, "report", "_cover.pdf")
body = os.path.join(ROOT, "report", "_body.pdf")
out_path = os.path.join(ROOT, "report", "frost-law-group-search-audit.pdf")
out = pymupdf.open()
for f in (cover, body):
    with pymupdf.open(f) as src:
        out.insert_pdf(src)
out.set_metadata({"title": "Frost Law Group Search Audit", "author": "Legal Leads Group", "subject": "Search Console audit and topical-authority plan", "creator": "Legal Leads Group"})
out.save(out_path, garbage=3, deflate=True)
print("merged", out_path, out.page_count, "pages")
out.close()
for f in (cover, body):
    os.remove(f)
