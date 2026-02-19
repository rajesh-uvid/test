# =============================================================================
# data.py — Static Configuration for UVID Email Signature Generator
# =============================================================================
# Edit this file to update URLs, defaults, and social links.
# No changes needed in app.py for routine updates.
# =============================================================================

# ── GitHub Repository Base ────────────────────────────────────────────────────
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/rajesh-uvid/test/refs/heads/main"

# ── Banner Configuration ──────────────────────────────────────────────────────
# URL to the JSON file that controls the active banner image and click link.
BANNER_CONFIG_URL    = f"{GITHUB_RAW_BASE}/banner_config.json"

# Fallback values used when banner_config.json cannot be fetched.
DEFAULT_BANNER_IMAGE = f"{GITHUB_RAW_BASE}/image/banner/banner.png"
DEFAULT_BANNER_LINK  = "https://www.uvidconsulting.com"

# ── Company Logo ──────────────────────────────────────────────────────────────
LOGO_URL = f"{GITHUB_RAW_BASE}/image/uvid/uvid.png"

# ── Social Media Icons ────────────────────────────────────────────────────────
LINKEDIN_URL  = f"{GITHUB_RAW_BASE}/image/socialMedia/linkedin.png"
YOUTUBE_URL   = f"{GITHUB_RAW_BASE}/image/socialMedia/youtube.png"
INSTAGRAM_URL = f"{GITHUB_RAW_BASE}/image/socialMedia/instagram.png"
EMPTY_URL     = f"{GITHUB_RAW_BASE}/image/socialMedia/empty.png"

# ── Social Media Profile Links ────────────────────────────────────────────────
LINKEDIN_PROFILE  = "https://www.linkedin.com/company/uvidconsulting"
YOUTUBE_PROFILE   = "https://www.youtube.com/@uvidconsulting"
INSTAGRAM_PROFILE = "https://www.instagram.com/uvidconsulting"

# ── Company Website ───────────────────────────────────────────────────────────
COMPANY_WEBSITE     = "https://www.uvidconsulting.com"
COMPANY_WEBSITE_DISPLAY = "www.uvidconsulting.com"
COMPANY_LOGO_LINK   = "https://uvidconsulting.com/"

# ── Signature Layout Dimensions ───────────────────────────────────────────────
LOGO_WIDTH       = 170    # px — logo image width
LOGO_COL_WIDTH   = 190    # px — logo table column width
ICON_SIZE        = 20     # px — social icon width & height
ICON_SPACER_W    = 8      # px — transparent spacer between icons
BANNER_WIDTH     = 580    # px — banner image width

# ── Input Field Default Placeholders ─────────────────────────────────────────
DEFAULT_NAME        = "Your Name"
DEFAULT_DESIGNATION = "Your Designation"
DEFAULT_EMAIL       = "mail@uvidconsulting.com"
