SITE = {
    "brand": "Voyages By Dave",
    "tagline": "Helping Canadians discover more of Canada",
    "url": "https://voyagesbydave.ca",
    "canonical_prefix": "https://voyagesbydave.ca/",
    "phone": "+1 (236) 258-8728",
    "phone_raw": "+12362588728",
    "email": "dave.rintoul@fora.travel",
    "location": "Fraser Valley, British Columbia, Canada",
    "fee": "$200",
    "currency": "CAD",
    "h1_default": "Canada Travel Advisor | Voyages By Dave",
    "description_default": (
        "Personal travel planning for Canadians exploring Canada, including "
        "accessible trips, multigenerational travel, rail journeys, road trips, "
        "cruises and complex itineraries."
    ),
    "primary_cta": "Plan my Canadian trip",
    "secondary_cta": "Explore how I can help",
    "review_cta": "Review my Canadian trip",
    "nav": [
        {"label": "Explore Canada", "slug": "canada", "children": [
            {"label": "British Columbia", "slug": "british-columbia"},
            {"label": "Canadian Rockies", "slug": "canadian-rockies"},
            {"label": "Canada by Rail", "slug": "canada-by-rail"},
            {"label": "Canadian Road Trips", "slug": "canadian-road-trips"},
            {"label": "Atlantic Canada", "slug": "atlantic-canada"},
            {"label": "Ontario & Quebec", "slug": "ontario-quebec"},
            {"label": "Northern Canada", "slug": "northern-canada"},
            {"label": "Canadian Cruises", "slug": "canadian-cruises"},
        ]},
        {"label": "Trip Types", "slug": "#trip-types", "children": [
            {"label": "Canada-Only Travel", "slug": "canada-only-travel"},
            {"label": "Accessible Travel", "slug": "accessible-travel-canada"},
            {"label": "Multigenerational", "slug": "multigenerational-canada"},
            {"label": "Adventure & Diving", "slug": "adventure-canada"},
        ]},
        {"label": "How I Work", "slug": "how-i-work"},
        {"label": "About Dave", "slug": "about"},
    ],
    "footer_nav": [
        {"label": "Home", "slug": ""},
        {"label": "Plan your trip", "slug": "plan"},
        {"label": "FAQ", "slug": "faq"},
        {"label": "How I Work", "slug": "how-i-work"},
        {"label": "About", "slug": "about"},
    ],
    "social": {
        "facebook": None,
        "instagram": None,
        "linkedin": None,
    },
    "profile_url": "https://www.davidrintoul.info",
    "fora_url": "https://www.foratravel.com/advisor/dave-rintoul",
    "cover_image": "https://davidrintoul.info/images/dave-antartica.webp",
}

# Convert relevant slug values to route paths
SITE["api_endpoint"] = "/api/plan"
SITE["plan_slug"] = "plan"
