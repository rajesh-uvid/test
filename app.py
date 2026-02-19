import streamlit as st
import streamlit.components.v1 as components
import requests

# ─────────────────────────────────────────────
# 1. Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="UVID Email Signature Generator",
    page_icon="✉️",
    layout="wide"
)

# ─────────────────────────────────────────────
# 2. Global CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        min-height: 100vh;
    }

    /* Header */
    .app-header {
        text-align: center;
        padding: 2rem 0 1.5rem 0;
    }
    .app-header h1 {
        font-size: 2.2rem;
        font-weight: 700;
        color: #f1f5f9;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .app-header p {
        color: #94a3b8;
        font-size: 1rem;
        margin-top: 0.4rem;
    }

    /* Card */
    .card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        backdrop-filter: blur(10px);
        margin-bottom: 1.5rem;
    }
    .card-title {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #64748b;
        margin-bottom: 1rem;
    }

    /* Inputs */
    .stTextInput > label {
        color: #cbd5e1 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 8px !important;
        color: #f1f5f9 !important;
        font-size: 0.9rem !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59,130,246,0.2) !important;
    }

    /* Section labels */
    .section-label {
        font-size: 1rem;
        font-weight: 600;
        color: #e2e8f0;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Preview wrapper */
    .preview-wrapper {
        background: #ffffff;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 4px 24px rgba(0,0,0,0.4);
    }

    /* Action buttons row */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #1d4ed8, #3b82f6) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.4rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        width: 100% !important;
        transition: all 0.2s !important;
    }
    .stDownloadButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 15px rgba(59,130,246,0.4) !important;
    }

    /* Info box */
    .info-box {
        background: rgba(59,130,246,0.1);
        border: 1px solid rgba(59,130,246,0.3);
        border-radius: 10px;
        padding: 0.8rem 1rem;
        color: #93c5fd;
        font-size: 0.82rem;
        line-height: 1.6;
    }

    /* Steps box */
    .steps-box {
        background: rgba(16,185,129,0.08);
        border: 1px solid rgba(16,185,129,0.25);
        border-radius: 10px;
        padding: 1rem 1.2rem;
        color: #6ee7b7;
        font-size: 0.83rem;
        line-height: 1.8;
    }
    .steps-box ol {
        margin: 0;
        padding-left: 1.2rem;
    }

    /* Hide streamlit elements */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 0 !important; max-width: 1200px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 3. Header
# ─────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <h1>✉️ UVID Email Signature Generator</h1>
    <p>Fill in your details below — your signature updates live in real time.</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 4. Input Form
# ─────────────────────────────────────────────
st.markdown('<div class="section-label">👤 Personal Details</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    name = st.text_input("Full Name", "Ali Khan", placeholder="e.g. Ali Khan")
with col2:
    designation = st.text_input("Designation", "Senior Consultant", placeholder="e.g. Senior Consultant")
with col3:
    email = st.text_input("Email Address", "ali@uvidconsulting.com", placeholder="ali@uvidconsulting.com")
with col4:
    phone = st.text_input("Phone Number (optional)", "", placeholder="+91 98765 43210")

# ─────────────────────────────────────────────────────────────────────────────
# Banner: Smart auto-detect — Vercel if live, else direct GitHub URLs
# ─────────────────────────────────────────────────────────────────────────────

BANNER_CONFIG_URL   = "https://raw.githubusercontent.com/rajesh-uvid/test/refs/heads/main/banner_config.json"
VERCEL_BASE_URL     = "https://test-uvid.vercel.app"   # ← update after Vercel deploy
VERCEL_IMAGE_EP     = f"{VERCEL_BASE_URL}/api/banner-image"
VERCEL_CLICK_EP     = f"{VERCEL_BASE_URL}/api/banner-click"

DEFAULT_BANNER_IMAGE = "https://raw.githubusercontent.com/rajesh-uvid/test/refs/heads/main/image/banner/banner.png"
DEFAULT_BANNER_LINK  = "https://www.uvidconsulting.com"


@st.cache_data(ttl=300)   # Re-evaluate every 5 minutes
def resolve_banner():
    """
    Priority 1 — Vercel is live: embed Vercel endpoints so the banner
                  is fully dynamic even in already-sent emails.
    Priority 2 — Vercel not deployed yet: fetch banner_config.json from
                  GitHub and embed the direct image/link URLs (static
                  but always up-to-date for newly generated signatures).
    Priority 3 — Everything fails: use hardcoded defaults.
    Returns (banner_url, banner_link, mode)
      mode = "vercel" | "github" | "default"
    """
    # ── Try Vercel ──────────────────────────────────────────────────────────
    try:
        probe = requests.head(VERCEL_IMAGE_EP, timeout=4, allow_redirects=True)
        if probe.status_code < 500:          # 200, 302 etc. → Vercel is live
            return (VERCEL_IMAGE_EP, VERCEL_CLICK_EP, "vercel", None, None)
    except Exception:
        pass

    # ── Try GitHub config ───────────────────────────────────────────────────
    try:
        r = requests.get(BANNER_CONFIG_URL, timeout=5)
        r.raise_for_status()
        cfg = r.json()
        img  = cfg.get("banner_image_url", DEFAULT_BANNER_IMAGE)
        link = cfg.get("banner_link_url",  DEFAULT_BANNER_LINK)
        return (img, link, "github", img, link)
    except Exception:
        pass

    # ── Hardcoded defaults ──────────────────────────────────────────────────
    return (DEFAULT_BANNER_IMAGE, DEFAULT_BANNER_LINK, "default",
            DEFAULT_BANNER_IMAGE, DEFAULT_BANNER_LINK)


BANNER_URL, BANNER_LINK, _mode, _cfg_img, _cfg_link = resolve_banner()

# ── Status badge ─────────────────────────────────────────────────────────────
if _mode == "vercel":
    st.markdown(f"""
    <div style="background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.3);
                border-radius:10px; padding:0.7rem 1.1rem; font-size:0.8rem;
                color:#6ee7b7; margin-bottom:0.8rem; line-height:1.8;">
        <strong>🟢 Mode: Vercel (fully dynamic)</strong><br>
        <span style="opacity:0.85;">
        Banner <code>src</code> &nbsp;→ <code style="color:#fde68a;">{VERCEL_IMAGE_EP}</code><br>
        Banner <code>href</code> → <code style="color:#fde68a;">{VERCEL_CLICK_EP}</code><br>
        ✅ <em>Already-sent emails will update automatically when you change
        <code>banner_config.json</code> on GitHub.</em>
        </span>
    </div>
    """, unsafe_allow_html=True)

elif _mode == "github":
    st.markdown(f"""
    <div style="background:rgba(59,130,246,0.08); border:1px solid rgba(59,130,246,0.3);
                border-radius:10px; padding:0.7rem 1.1rem; font-size:0.8rem;
                color:#93c5fd; margin-bottom:0.8rem; line-height:1.8;">
        <strong>🔵 Mode: GitHub config (static URLs in signature)</strong><br>
        <span style="opacity:0.85;">
        Vercel not detected — using direct URLs from <code>banner_config.json</code>.<br>
        Banner image → <code style="color:#bfdbfe;">{_cfg_img}</code><br>
        Banner link &nbsp;→ <code style="color:#bfdbfe;">{_cfg_link}</code><br>
        ⚠️ <em>Already-sent emails won't update. Deploy to Vercel for dynamic banners.</em>
        </span>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="background:rgba(239,68,68,0.08); border:1px solid rgba(239,68,68,0.3);
                border-radius:10px; padding:0.7rem 1.1rem; font-size:0.8rem;
                color:#fca5a5; margin-bottom:0.8rem;">
        <strong>🔴 Mode: Defaults (no config reachable)</strong><br>
        Using hardcoded fallback URLs. Check your internet / GitHub repo visibility.
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 5. Build the Signature HTML
# ─────────────────────────────────────────────
phone_html = (
    f'<span style="display:block; margin-bottom:3px; font-size:10pt; color:#333333;">'
    f'{phone}</span>'
) if phone and phone.strip() else ""

LOGO_URL      = "https://raw.githubusercontent.com/rajesh-uvid/test/refs/heads/main/image/uvid/uvid.png"
LINKEDIN_URL  = "https://raw.githubusercontent.com/rajesh-uvid/test/refs/heads/main/image/socialMedia/linkedin.png"
YOUTUBE_URL   = "https://raw.githubusercontent.com/rajesh-uvid/test/refs/heads/main/image/socialMedia/youtube.png"
INSTAGRAM_URL = "https://raw.githubusercontent.com/rajesh-uvid/test/refs/heads/main/image/socialMedia/instagram.png"

sig_html = f"""<table cellpadding="0" cellspacing="0" border="0"
    style="font-family: 'Roboto', Arial, sans-serif; font-weight:400; color: #333333; width: 600px;
           border-collapse: collapse; table-layout: fixed;">

    <!-- Row 1: Logo + Info -->
    <tr>
        <td valign="middle" style="padding: 0 16px 0 0; width: 190px;">
            <a href="https://uvidconsulting.com/" target="_blank" style="text-decoration:none;">
                <img src="{LOGO_URL}"
                     alt="UVID Consulting" width="180"
                     style="display:block; border:0; outline:none; text-decoration:none;">
            </a>
        </td>
        <td valign="middle"
            style="border-left: 2px solid #cccccc; padding-left: 16px;">

            <!-- Name -->
            <div style="font-size:13pt; font-weight:400; color:#000000; margin-bottom:0px; line-height:1.4;">
                {name}
            </div>

            <!-- Designation -->
            <div style="font-size:10pt; font-weight:400; color:#555555; margin-bottom:4px; line-height:1.4;">
                {designation}
            </div>

            <!-- Contact -->
            <div style="font-size:10pt; font-weight:400; color:#333333; line-height:1.5;">
                {phone_html}
                <a href="mailto:{email}"
                   style="color:#333333; text-decoration:none; display:block; font-weight:400;">{email}</a>
                <a href="https://www.uvidconsulting.com"
                   style="color:#333333; text-decoration:none; display:block; font-weight:400;">
                   www.uvidconsulting.com
                </a>
            </div>

            <!-- Social Icons: forced equal height via table cell -->
            <div style="margin-top:8px; line-height:0; font-size:0;">
                <a href="https://www.linkedin.com/company/uvidconsulting" target="_blank"
                   style="text-decoration:none; display:inline-block; margin-right:6px;">
                    <img src="{LINKEDIN_URL}" alt="LinkedIn"
                         width="28" height="28"
                         style="display:block; border:0; width:28px; height:28px;">
                </a>
                <a href="https://www.youtube.com/@uvidconsulting" target="_blank"
                   style="text-decoration:none; display:inline-block; margin-right:6px;">
                    <img src="{YOUTUBE_URL}" alt="YouTube"
                         width="28" height="28"
                         style="display:block; border:0; width:28px; height:28px;">
                </a>
                <a href="https://www.instagram.com/uvidconsulting" target="_blank"
                   style="text-decoration:none; display:inline-block;">
                    <img src="{INSTAGRAM_URL}" alt="Instagram"
                         width="28" height="28"
                         style="display:block; border:0; width:28px; height:28px;">
                </a>
            </div>
        </td>
    </tr>

    <!-- Row 2: Banner (no gap) -->
    <tr>
        <td colspan="2" style="padding-top: 0; margin: 10px; line-height:0; font-size:0;">
            <a href="{BANNER_LINK}" target="_blank" style="display:block;">
                <img src="{BANNER_URL}"
                     alt="UVID Consulting Banner"
                     width="600"
                     style="display:block; width:600px; height:auto; border:0; outline:none; margin:0;">
            </a>
        </td>
    </tr>

</table>"""

# Full standalone HTML for download
full_html = f"""<!DOCTYPE html>
<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</head>
<body style="margin:0; padding:20px; background:#ffffff;">
{sig_html}
</body>
</html>"""

# ─────────────────────────────────────────────
# 6. Live Preview + Actions
# ─────────────────────────────────────────────
st.markdown('<div class="section-label">👁️ Live Signature Preview</div>', unsafe_allow_html=True)

# Full iframe rendering (proper render — no HTML sanitization)
preview_and_copy = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap" rel="stylesheet">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: 'Roboto', Arial, sans-serif;
    font-weight: 400;
    background: #ffffff;
    padding: 24px 24px 16px 24px;
  }}
  .sig-wrapper {{
    display: block;
  }}
  .actions {{
    margin-top: 16px;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    align-items: center;
  }}
  button {{
    padding: 9px 22px;
    font-size: 13px;
    font-weight: 500;
    border: none;
    border-radius: 7px;
    cursor: pointer;
    transition: all 0.2s ease;
    font-family: 'Roboto', Arial, sans-serif;
    letter-spacing: 0.2px;
  }}
  #copyBtn {{
    background: linear-gradient(135deg, #1d4ed8, #3b82f6);
    color: #ffffff;
    box-shadow: 0 2px 8px rgba(59,130,246,0.35);
  }}
  #copyBtn:hover {{ opacity: 0.88; transform: translateY(-1px); }}
  #copyBtn.success {{
    background: linear-gradient(135deg, #059669, #10b981);
    box-shadow: 0 2px 8px rgba(16,185,129,0.35);
  }}
  .note {{
    margin-top: 10px;
    font-size: 11.5px;
    color: #64748b;
    line-height: 1.5;
  }}
</style>
</head>
<body>

<div class="sig-wrapper" id="sig">
{sig_html}
</div>

<div class="actions">
  <button id="copyBtn" onclick="copySignature()">&#128203; Copy Signature for Outlook</button>
</div>

<p class="note">
  &#10003; Click above &rarr; open Outlook &rarr; New Signature &rarr; paste with <strong>Ctrl+V</strong>
</p>

<script>
async function copySignature() {{
  const btn = document.getElementById('copyBtn');
  const sigEl = document.getElementById('sig');

  try {{
    const htmlContent = sigEl.innerHTML;
    const blob = new Blob([htmlContent], {{ type: 'text/html' }});
    const plainText = sigEl.innerText;
    const textBlob = new Blob([plainText], {{ type: 'text/plain' }});
    const clipItem = new ClipboardItem({{
      'text/html': blob,
      'text/plain': textBlob
    }});
    await navigator.clipboard.write([clipItem]);
    showSuccess(btn, '&#10003; Copied! Paste in Outlook');
  }} catch(e) {{
    try {{
      const range = document.createRange();
      range.selectNodeContents(sigEl);
      const sel = window.getSelection();
      sel.removeAllRanges();
      sel.addRange(range);
      document.execCommand('copy');
      sel.removeAllRanges();
      showSuccess(btn, '&#10003; Copied! Paste in Outlook');
    }} catch(e2) {{
      btn.textContent = 'Copy failed — use Download instead';
      btn.style.background = '#dc2626';
    }}
  }}
}}

function showSuccess(btn, msg) {{
  const original = btn.innerHTML;
  btn.innerHTML = msg;
  btn.classList.add('success');
  setTimeout(() => {{
    btn.innerHTML = original;
    btn.classList.remove('success');
  }}, 3000);
}}
</script>
</body>
</html>
"""

# Render the preview inside an iframe
components.html(preview_and_copy, height=560, scrolling=False)

# ─────────────────────────────────────────────
# 7. Download Button
# ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-label">⬇️ Download & Instructions</div>', unsafe_allow_html=True)

dl_col, info_col = st.columns([1, 2])

with dl_col:
    st.download_button(
        label="⬇️ Download Signature (.html)",
        data=full_html.encode("utf-8"),
        file_name=f"signature_{name.replace(' ', '_').lower()}.html",
        mime="text/html",
        help="Download the HTML file, open in browser, select all, then paste into Outlook"
    )
    st.markdown("""
    <div style="margin-top:10px; font-size:0.78rem; color:#64748b; line-height:1.6;">
        Alternate method if copy button doesn't work.
    </div>
    """, unsafe_allow_html=True)

with info_col:
    st.markdown("""
    <div class="steps-box">
        <strong style="color:#34d399;">📌 How to add this signature in Outlook:</strong><br>
        <ol>
            <li>Click <strong>"📋 Copy Signature for Outlook"</strong> above</li>
            <li>Open <strong>Outlook</strong> → File → Options → Mail → <strong>Signatures</strong></li>
            <li>Click <strong>New</strong> → give it a name → paste with <strong>Ctrl+V</strong></li>
            <li>Click <strong>OK</strong> and assign it as your default signature</li>
        </ol>
        <br>
        <strong style="color:#34d399;">💡 Alternative (Download method):</strong><br>
        Download the .html → open in Chrome/Edge → Select All (Ctrl+A) → Copy → Paste in Outlook signature editor
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 8. Raw HTML Code (for manual use)
# ─────────────────────────────────────────────
with st.expander("🔧 View Raw HTML Code (for advanced users)", expanded=False):
    st.markdown("""
    <div class="info-box">
        ✅ <strong>All images are .png</strong> — fully compatible with Outlook.
        Copy the HTML below or use the Download button to get your signature file.
    </div>
    """, unsafe_allow_html=True)
    st.code(sig_html, language="html")