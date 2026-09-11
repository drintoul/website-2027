#!/usr/bin/env python3
"""Generate static HTML pages and supporting files for Voyages By Dave."""

import json
import html
import re
import os
import shutil
import sys
import datetime

# Import site config and page content from sibling modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_config import SITE
from pages import PAGES


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Stable canonical entity identifiers
AGENCY_ID = SITE["url"] + "/#travelagency"
WEBSITE_ID = SITE["url"] + "/#website"
AREA_CANADA_ID = SITE["url"] + "/#area/canada"
PERSON_ID = SITE["url"] + "/about/#dave"

BUSINESS_DESCRIPTION = (
    "Personal travel planning for Canadians whose trips benefit from careful research, "
    "comparison, verification and professional judgment. Voyages By Dave specializes in "
    "Canadian travel, accessible and multigenerational trips, cruises, adventure and diving "
    "travel, and complex itineraries, combining personally developed research technology with "
    "professional travel relationships and advisor support."
)

SLOGAN = "Canada is the destination. Dave makes it work."

KNOWS_ABOUT = [
    "Canadian travel",
    "British Columbia travel",
    "Canadian Rockies travel",
    "Canada rail travel",
    "Canadian road trips",
    "Canadian cruises",
    "Accessible travel",
    "Multigenerational travel",
    "Adventure travel",
    "Diving travel",
    "Expedition travel",
    "Complex itineraries",
    "Multi-destination travel",
    "Travel logistics",
    "Travel research",
]


def write(path, content):
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else BASE_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def clean_text(text):
    return " ".join(text.split())


def build_jsonld(page, canonical):
    """Build the home-page @graph: WebSite, WebPage and primary TravelAgency entity."""
    agency = {
        "@type": "TravelAgency",
        "@id": AGENCY_ID,
        "name": SITE["brand"],
        "url": SITE["url"],
        "logo": SITE["url"] + "/favicon-2026.svg",
        "image": SITE["cover_image"],
        "description": BUSINESS_DESCRIPTION,
        "slogan": SLOGAN,
        "telephone": SITE["phone_raw"],
        "email": SITE["email"],
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Fraser Valley",
            "addressRegion": "BC",
            "addressCountry": "CA",
        },
        "areaServed": {
            "@type": "Country",
            "@id": AREA_CANADA_ID,
            "name": "Canada",
        },
        "sameAs": [
            SITE["profile_url"],
            SITE["fora_url"],
        ],
        "knowsAbout": KNOWS_ABOUT,
        "founder": {"@id": PERSON_ID},
        "makesOffer": [
            {
                "@type": "Offer",
                "@id": SITE["url"] + "/#offer/personal-travel-planning",
                "itemOffered": {
                    "@type": "Service",
                    "@id": SITE["url"] + "/#service/personal-travel-planning",
                    "name": "Personal Travel Planning",
                    "description": "Research, comparison, and itinerary planning for travelers whose trips benefit from professional research, verification, and judgment.",
                    "provider": {"@id": AGENCY_ID},
                    "areaServed": {"@id": AREA_CANADA_ID},
                },
            },
            {
                "@type": "Offer",
                "@id": SITE["url"] + "/#offer/complex-itinerary-planning",
                "itemOffered": {
                    "@type": "Service",
                    "@id": SITE["url"] + "/#service/complex-itinerary-planning",
                    "name": "Complex Itinerary Planning",
                    "description": "Planning and coordination for multi-destination, accessibility-sensitive, multigenerational, or otherwise complex journeys where transportation, timing, and logistics need to work together.",
                    "provider": {"@id": AGENCY_ID},
                    "areaServed": {"@id": AREA_CANADA_ID},
                },
            },
            {
                "@type": "Offer",
                "@id": SITE["url"] + "/#offer/travel-research-verification",
                "itemOffered": {
                    "@type": "Service",
                    "@id": SITE["url"] + "/#service/travel-research-verification",
                    "name": "Travel Research and Verification",
                    "description": "Research and cross-checking of destinations, transportation, accommodations, cruises, accessibility information, and other travel details using current sources and personally developed research technology.",
                    "provider": {"@id": AGENCY_ID},
                    "areaServed": {"@id": AREA_CANADA_ID},
                },
            },
            {
                "@type": "Offer",
                "@id": SITE["url"] + "/#offer/professional-travel-access-support",
                "itemOffered": {
                    "@type": "Service",
                    "@id": SITE["url"] + "/#service/professional-travel-access-support",
                    "name": "Professional Travel Access and Support",
                    "description": "Travel planning and booking supported by professional travel relationships, advisor resources, and industry connections that may provide additional recognition, amenities, benefits, experiences, or support when available.",
                    "provider": {"@id": AGENCY_ID},
                    "areaServed": {"@id": AREA_CANADA_ID},
                },
            },
        ],
    }

    website = {
        "@type": "WebSite",
        "@id": WEBSITE_ID,
        "url": SITE["url"],
        "name": SITE["brand"],
        "publisher": {"@id": AGENCY_ID},
    }

    webpage = {
        "@type": "WebPage",
        "@id": canonical + "#webpage",
        "url": canonical,
        "name": page.get("title") or SITE["brand"],
        "description": clean_text(page.get("description") or SITE["description_default"]),
        "isPartOf": {"@id": WEBSITE_ID},
        "mainEntity": {"@id": AGENCY_ID},
    }

    data = {
        "@context": "https://schema.org",
        "@graph": [website, webpage, agency],
    }
    return "<script type=\"application/ld+json\">\n" + json.dumps(data, indent=2) + "\n</script>"


def build_faq_jsonld(page, canonical):
    """Build FAQ page schema referencing the primary TravelAgency and WebSite."""
    main_entity = []
    content = page["content"]
    for m in re.finditer(r'<details class="faq-item">\s*<summary>(.*?)</summary>\s*(.*?)\s*</details>', content, re.DOTALL):
        question = m.group(1).strip()
        answer_html = m.group(2)
        answer_parts = re.findall(r'<p[^>]*>(.*?)</p>', answer_html, re.DOTALL)
        answer = " ".join(html.unescape(re.sub(r'<[^>]+>', '', part)) for part in answer_parts)
        answer = clean_text(answer)
        main_entity.append({
            "@type": "Question",
            "name": question,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": answer,
            },
        })

    faq_page = {
        "@type": "FAQPage",
        "@id": canonical + "#webpage",
        "url": canonical,
        "name": page.get("title") or SITE["brand"],
        "description": clean_text(page.get("description") or SITE["description_default"]),
        "isPartOf": {"@id": WEBSITE_ID},
        "about": {"@id": AGENCY_ID},
        "mainEntity": main_entity,
    }

    data = {
        "@context": "https://schema.org",
        "@graph": [faq_page],
    }
    return "<script type=\"application/ld+json\">\n" + json.dumps(data, indent=2) + "\n</script>"


def build_about_jsonld(page, canonical):
    """Build the About page schema with a Person as mainEntity."""
    lead_match = re.search(r'<p class="lead">(.*?)</p>', page["content"], re.DOTALL)
    person_description = (
        clean_text(html.unescape(re.sub(r'<[^>]+>', '', lead_match.group(1))))
        if lead_match
        else "Canadian travel advisor based in British Columbia's Fraser Valley."
    )

    person = {
        "@type": "Person",
        "@id": PERSON_ID,
        "name": "Dave Rintoul",
        "url": canonical,
        "jobTitle": "Canadian travel advisor and trip planner",
        "description": person_description,
        "sameAs": [SITE["profile_url"]],
        "knowsAbout": KNOWS_ABOUT,
        "worksFor": {"@id": AGENCY_ID},
    }

    webpage = {
        "@type": "WebPage",
        "@id": canonical + "#webpage",
        "url": canonical,
        "name": page.get("title") or SITE["brand"],
        "description": clean_text(page.get("description") or SITE["description_default"]),
        "isPartOf": {"@id": WEBSITE_ID},
        "about": {"@id": AGENCY_ID},
        "mainEntity": person,
    }

    data = {
        "@context": "https://schema.org",
        "@graph": [webpage],
    }
    return "<script type=\"application/ld+json\">\n" + json.dumps(data, indent=2) + "\n</script>"


def build_webpage_jsonld(page, canonical):
    """Build a generic WebPage schema that references the primary business entity."""
    webpage = {
        "@type": "WebPage",
        "@id": canonical + "#webpage",
        "url": canonical,
        "name": page.get("title") or SITE["brand"],
        "description": clean_text(page.get("description") or SITE["description_default"]),
        "isPartOf": {"@id": WEBSITE_ID},
        "about": {"@id": AGENCY_ID},
    }

    data = {
        "@context": "https://schema.org",
        "@graph": [webpage],
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

    if slug == "":
        jsonld = build_jsonld(page, canonical)
    elif slug == "faq":
        jsonld = build_faq_jsonld(page, canonical)
    elif slug == "about":
        jsonld = build_about_jsonld(page, canonical)
    else:
        jsonld = build_webpage_jsonld(page, canonical)

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
