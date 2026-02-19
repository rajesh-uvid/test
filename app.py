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
    name = st.text_input("Full Name", "Your Name", placeholder="e.g. Ali Khan")
with col2:
    designation = st.text_input("Designation", "Your Designation", placeholder="e.g. Senior Consultant")
with col3:
    email = st.text_input("Email Address", "mail@uvidconsulting.com", placeholder="mail@uvidconsulting.com")
with col4:
    phone = st.text_input("Phone Number (optional)", "", placeholder="+91 8888888888")

# ─────────────────────────────────────────────────────────────────────────────
# Banner Mode Selector
# ─────────────────────────────────────────────────────────────────────────────

BANNER_CONFIG_URL    = "https://raw.githubusercontent.com/rajesh-uvid/test/refs/heads/main/banner_config.json"
DEFAULT_BANNER_IMAGE = "https://raw.githubusercontent.com/rajesh-uvid/test/refs/heads/main/image/banner/banner.png"
DEFAULT_BANNER_LINK  = "https://www.uvidconsulting.com"

st.markdown('<div class="section-label">🖼️ Banner Mode</div>', unsafe_allow_html=True)

_spacer, _radio_col = st.columns([3, 2])
with _radio_col:
    banner_mode = st.radio(
        "Banner source:",
        ["🔵 GitHub (default)",
         "🟢 Vercel (dynamic)"],
        horizontal=True,
        help="GitHub: fetches banner_config.json. Vercel: fully dynamic in sent emails."
    )

use_vercel = banner_mode.startswith("🟢")

# ── GitHub mode ───────────────────────────────────────────────────────────────
if not use_vercel:

    @st.cache_data(ttl=300)
    def fetch_github_banner():
        try:
            r = requests.get(BANNER_CONFIG_URL, timeout=5)
            r.raise_for_status()
            cfg = r.json()
            return (
                cfg.get("banner_image_url", DEFAULT_BANNER_IMAGE),
                cfg.get("banner_link_url",  DEFAULT_BANNER_LINK),
                True
            )
        except Exception:
            return (DEFAULT_BANNER_IMAGE, DEFAULT_BANNER_LINK, False)

    BANNER_URL, BANNER_LINK, _ok = fetch_github_banner()

    if _ok:
        st.markdown(f"""
        <div style="background:rgba(59,130,246,0.08); border:1px solid rgba(59,130,246,0.3);
                    border-radius:10px; padding:0.65rem 1rem; font-size:0.79rem;
                    color:#93c5fd; margin-top:0.5rem; line-height:1.8;">
            <strong>🔵 GitHub mode — fetched from <code>banner_config.json</code></strong><br>
            <span style="opacity:0.85;">
            Image &nbsp;→ <code style="color:#bfdbfe;">{BANNER_URL}</code><br>
            Link &nbsp;&nbsp;&nbsp;→ <code style="color:#bfdbfe;">{BANNER_LINK}</code><br>
            To change: edit <code>banner_config.json</code> on GitHub and push.
            New signatures will pick it up within 5 min.
            </span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:rgba(239,68,68,0.08); border:1px solid rgba(239,68,68,0.3);
                    border-radius:10px; padding:0.65rem 1rem; font-size:0.79rem;
                    color:#fca5a5; margin-top:0.5rem;">
            ⚠️ Could not fetch <code>banner_config.json</code> from GitHub — using defaults.
        </div>
        """, unsafe_allow_html=True)

# ── Vercel mode ────────────────────────────────────────────────────────────────
else:
    vercel_url = st.text_input(
        "Your Vercel project URL",
        placeholder="https://your-project.vercel.app",
        help="Paste the URL you get after deploying this repo to vercel.com"
    ).rstrip("/")

    if vercel_url:
        BANNER_URL  = f"{vercel_url}/api/banner-image"
        BANNER_LINK = f"{vercel_url}/api/banner-click"
        st.markdown(f"""
        <div style="background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.3);
                    border-radius:10px; padding:0.65rem 1rem; font-size:0.79rem;
                    color:#6ee7b7; margin-top:0.5rem; line-height:1.8;">
            <strong>🟢 Vercel mode — fully dynamic banners in sent emails</strong><br>
            <span style="opacity:0.85;">
            Image src &nbsp;→ <code style="color:#fde68a;">{BANNER_URL}</code><br>
            Click href → <code style="color:#fde68a;">{BANNER_LINK}</code><br>
            ✅ Changing <code>banner_config.json</code> on GitHub updates the banner
            in <em>every already-sent email</em> automatically.
            </span>
        </div>
        """, unsafe_allow_html=True)
    else:
        # No Vercel URL yet — fall back to GitHub config silently
        @st.cache_data(ttl=300)
        def fetch_github_banner_fallback():
            try:
                r = requests.get(BANNER_CONFIG_URL, timeout=5)
                r.raise_for_status()
                cfg = r.json()
                return (cfg.get("banner_image_url", DEFAULT_BANNER_IMAGE),
                        cfg.get("banner_link_url",  DEFAULT_BANNER_LINK))
            except Exception:
                return (DEFAULT_BANNER_IMAGE, DEFAULT_BANNER_LINK)

        BANNER_URL, BANNER_LINK = fetch_github_banner_fallback()
        st.markdown("""
        <div style="background:rgba(251,191,36,0.08); border:1px solid rgba(251,191,36,0.3);
                    border-radius:10px; padding:0.65rem 1rem; font-size:0.79rem;
                    color:#fde68a; margin-top:0.5rem;">
            ⏳ Enter your Vercel URL above to enable dynamic banners.<br>
            Using GitHub config URLs as a preview fallback for now.
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
EMPTY_URL     = "https://raw.githubusercontent.com/rajesh-uvid/test/refs/heads/main/image/socialMedia/empty.png"

phone_line = f'<span style="color:#000000; font-family:Roboto,sans-serif; font-size:9pt;">{phone}</span><br />' if phone and phone.strip() else ""

sig_html = f"""<table cellspacing="0" cellpadding="0" border="0">
  <tbody>
    <tr>

      <!-- LEFT: Logo — vertically & horizontally centered -->
      <td width="190" valign="middle" align="center"
          style="padding:0 10px 0 0; width:190px;">
        <a href="https://uvidconsulting.com/" target="_blank">
          <img src="{LOGO_URL}"
               nosend="1" border="0"
               width="170" alt="UVID Consulting"
               style="display:block; border:0; width:170px; height:auto;" />
        </a>
      </td>

      <!-- DIVIDER: bgcolor attribute (Outlook Classic safe, no border-left) -->
      <td width="1" bgcolor="#cccccc"
          style="width:1px; padding:0; font-size:0; line-height:0;">
      </td>

      <!-- RIGHT: Info column -->
      <td valign="top" style="padding:0 0 0 8px;">

        <!-- Name -->
        <span style="color:#000000; font-family:Roboto,sans-serif; font-size:12pt; font-weight:bold;">{name}</span><br />

        <!-- Designation -->
        <span style="color:#555555; font-family:Roboto,sans-serif; font-size:10pt;">{designation}</span><br />

        <!-- Phone (optional) -->
        {phone_line}

        <!-- Email -->
        <a href="mailto:{email}" style="text-decoration:none;">
          <span style="color:#000000; font-family:Roboto,sans-serif; font-size:9pt;">{email}</span>
        </a><br />

        <!-- Website -->
        <a href="https://www.uvidconsulting.com" target="_blank" style="text-decoration:none;">
          <span style="color:#000000; font-family:Roboto,sans-serif; font-size:9pt;">www.uvidconsulting.com</span>
        </a><br /><br />
        <!-- Social Icons: border=0 + text-decoration:none kills Outlook underline -->
        <a href="https://www.linkedin.com/company/uvidconsulting" target="_blank"
           style="text-decoration:none; border:0;">
          <img src="{LINKEDIN_URL}" nosend="1" border="0"
               width="18" height="18" alt="LinkedIn"
               style="border:0; vertical-align:bottom; width:18px; height:18px;" />
        </a><img src="{EMPTY_URL}" nosend="1" border="0"
               width="8" height="1"
               style="border:0; vertical-align:bottom;" /><a href="https://www.youtube.com/@uvidconsulting" target="_blank"
           style="text-decoration:none; border:0;">
          <img src="{YOUTUBE_URL}" nosend="1" border="0"
               width="20" height="18" alt="YouTube"
               style="border:0; vertical-align:bottom; width:18px; height:18px;" />
        </a><img src="{EMPTY_URL}" nosend="1" border="0"
               width="8" height="1"
               style="border:0; vertical-align:bottom;" /><a href="https://www.instagram.com/uvidconsulting" target="_blank"
           style="text-decoration:none; border:0;">
          <img src="{INSTAGRAM_URL}" nosend="1" border="0"
               width="18" height="18" alt="Instagram"
               style="border:0; vertical-align:bottom; width:18px; height:18px;" />
        </a>

      </td>
    </tr>
  </tbody>
</table>

<br />

<!-- Banner: separate table -->
<table cellspacing="0" cellpadding="0" border="0">
  <tbody>
    <tr>
      <td valign="top" style="padding:0; line-height:0; font-size:0;">
        <a href="{BANNER_LINK}" target="_blank">
          <img src="{BANNER_URL}"
               nosend="1" border="0"
               width="580" height="auto"
               alt="UVID Consulting Banner"
               style="display:block; border:0; width:580px; height:auto;" />
        </a>
      </td>
    </tr>
  </tbody>
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
    font-family: 'Roboto', Roboto, sans-serif;
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
    font-family: 'Roboto', Roboto, sans-serif;
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