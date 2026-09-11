#!/usr/bin/env python3
"""Generate static HTML pages and supporting files for Voyages By Dave."""

import json
import os
import shutil
import sys
import datetime

# Import site config and page content from sibling modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_config import SITE
from pages import PAGES


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def write(path, content):
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else BASE_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def clean_text(text):
    return " ".join(text.split())


def build_jsonld():
    data = {
        "@context": "https://schema.org",
        "@type": "TravelAgency",
        "name": SITE["brand"],
        "url": SITE["url"],
        "logo": SITE["url"] + "/favicon-2026.svg",
        "description": SITE["description_default"],
        "areaServed": {
            "@type": "Country",
            "name": "Canada",
        },
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Fraser Valley",
            "addressRegion": "BC",
            "addressCountry": "CA",
        },
        "telephone": SITE["phone_raw"],
        "email": SITE["email"],
        "image": SITE["cover_image"],
        "sameAs": [
            SITE["profile_url"],
            SITE["fora_url"],
        ],
    }
    return "<script type=\"application/ld+json\">\n" + json.dumps(data, indent=2) + "\n</script>"


def render_page(page):
    template_path = os.path.join(os.path.dirname(__file__), "template.html")
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    title = page.get("title") or SITE["brand"]
    description = clean_text(page.get("description") or SITE["description_default"])
    slug = page["slug"]
    canonical = SITE["url"] + "/" + (slug + "/" if slug else "")
    slug_class = "home" if not slug else slug
    body_class = page.get("body_class", "page-sub") + f" page-{slug_class}"
    content = page["content"].strip()

    jsonld = build_jsonld() if slug == "" else ""

    html = template
    for key, value in {
        "%TITLE%": title,
        "%DESCRIPTION%": description,
        "%CANONICAL%": canonical,
        "%CONTENT%": content,
        "%BODY_CLASS%": body_class,
        "%JSONLD%": jsonld,
        "%PHONE%": SITE["phone"],
        "%PHONE_RAW%": SITE["phone_raw"],
        "%EMAIL%": SITE["email"],
        "%FEE%": SITE["fee"],
        "%YEAR%": str(datetime.date.today().year),
        "%PROFILE_URL%": SITE["profile_url"],
        "%FORA_URL%": SITE["fora_url"],
        "%COVER_IMAGE%": SITE["cover_image"],
    }.items():
        html = html.replace(key, value)
    return html


def generate_config_js():
    config = {
        "brand": SITE["brand"],
        "tagline": SITE["tagline"],
        "url": SITE["url"],
        "phone": SITE["phone"],
        "phone_raw": SITE["phone_raw"],
        "email": SITE["email"],
        "location": SITE["location"],
        "fee": SITE["fee"],
        "primary_cta": SITE["primary_cta"],
        "secondary_cta": SITE["secondary_cta"],
        "review_cta": SITE["review_cta"],
        "api_endpoint": SITE["api_endpoint"],
        "year": datetime.date.today().year,
    }
    return "window.SITE = " + json.dumps(config, indent=2) + ";\n"


def generate_sitemap():
    today = datetime.date.today().isoformat()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for page in PAGES:
        loc = SITE["url"] + "/" + (page["slug"] + "/" if page["slug"] else "")
        priority = page.get("priority", 0.5)
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        lines.append(f"    <lastmod>{today}</lastmod>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines)


def generate_robots():
    return f"""User-agent: *
Allow: /
Sitemap: {SITE['url']}/sitemap.xml
"""


def main():
    for page in PAGES:
        slug = page["slug"]
        if slug == "":
            out_path = os.path.join(BASE_DIR, "index.html")
        else:
            out_path = os.path.join(BASE_DIR, slug, "index.html")
        html = render_page(page)
        write(out_path, html)
        print(f"Wrote {out_path}")

    write(os.path.join(BASE_DIR, "config.js"), generate_config_js())
    write(os.path.join(BASE_DIR, "sitemap.xml"), generate_sitemap())
    write(os.path.join(BASE_DIR, "robots.txt"), generate_robots())

    src_dir = os.path.dirname(__file__)
    for asset in ("style.css", "site.js", "favicon-2026.svg"):
        src = os.path.join(src_dir, asset)
        if os.path.exists(src):
            dst = os.path.join(BASE_DIR, asset)
            shutil.copy2(src, dst)
            print(f"Copied {asset} to site root")

    print("Generated config.js, sitemap.xml, robots.txt")


if __name__ == "__main__":
    main()
