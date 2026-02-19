# ✉️ UVID Email Signature Generator

A Streamlit app that generates professional, Outlook-ready HTML email signatures with a **dynamic banner system** — update the banner image or click link anytime, and it reflects in already-sent emails.

---

## 🚀 Features

- 📝 Fill in name, designation, email, phone (optional)
- 👁️ Live signature preview rendered in real time
- 📋 One-click **Copy for Outlook** button (paste directly into Outlook signature editor)
- ⬇️ Download as `.html` file
- 🖼️ **Dynamic banner** — change banner image & redirect link without resending emails
- 🔵 **GitHub mode** — banner config stored in `banner_config.json`
- 🟢 **Vercel mode** — fully dynamic banners that update in already-sent emails

---

## 📦 Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/rajesh-uvid/test.git
cd test

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

App opens at: **http://localhost:8501**

---

## 🖼️ Banner Config (GitHub Mode)

Banner image and click link are controlled by **`banner_config.json`** in the root of this repo:

```json
{
  "banner_image_url": "https://raw.githubusercontent.com/rajesh-uvid/test/refs/heads/main/image/banner/banner.png",
  "banner_link_url": "https://www.uvidconsulting.com"
}
```

### To change the banner:
1. Edit `banner_config.json`
2. Update `banner_image_url` → URL of your new banner image (must be publicly accessible)
3. Update `banner_link_url` → URL you want the banner to link to
4. Push to GitHub:
   ```bash
   git add banner_config.json
   git commit -m "Update banner for new campaign"
   git push
   ```
5. The Streamlit app picks up the change within **5 minutes** (cached)

> ⚠️ In GitHub mode, only **newly generated signatures** use the new banner.  
> Already-sent emails are not affected. Use **Vercel mode** for that.

---

## 🟢 Vercel Mode — Dynamic Banners in Sent Emails

When deployed to Vercel, the banner `src` and click `href` in the signature point to **Vercel serverless functions**. Every time a recipient opens the email, Vercel fetches the latest `banner_config.json` and serves the current banner — **even in emails sent months ago**.

### One-Time Vercel Setup

**Step 1 — Deploy to Vercel:**
1. Go to [vercel.com](https://vercel.com) and sign in with GitHub
2. Click **"Add New Project"** → Import `rajesh-uvid/test`
3. Leave all settings as default → click **Deploy**
4. Copy your project URL (e.g., `https://test-abc123.vercel.app`)

**Step 2 — Update `app.py`:**

Find this line in `app.py` (around line 200) and replace the placeholder:

```python
# Before
VERCEL_BASE_URL = "https://test-uvid.vercel.app"

# After — paste your actual Vercel URL
VERCEL_BASE_URL = "https://test-abc123.vercel.app"
```

Push the change:
```bash
git add app.py
git commit -m "Set Vercel base URL"
git push
```

Vercel automatically redeploys on every push.

**Step 3 — Use Vercel mode in the app:**
1. Open the Streamlit app
2. Select **🟢 Vercel (dynamic)** radio button
3. Paste your Vercel URL in the text field
4. Generate and copy your signature — it now uses the Vercel endpoints

---

## 🔄 Changing Banner/Link After Setup (Vercel Mode)

Once deployed, you **never need to touch `app.py` again**. Just update the config:

```json
// banner_config.json — update these two values
{
  "banner_image_url": "https://your-server.com/new-campaign-banner.png",
  "banner_link_url":  "https://your-landing-page.com/campaign-2026"
}
```

```bash
git add banner_config.json
git commit -m "Switch to Q2 campaign banner"
git push
```

✅ **All sent emails** — next time any recipient opens them → new banner, new link. Done.

---

## 📁 Project Structure

```
test/
├── app.py                    # Streamlit signature generator app
├── banner_config.json        # ← Edit this to change banner image & link
├── requirements.txt          # Python dependencies
├── vercel.json               # Vercel deployment config
├── api/
│   ├── banner-image.js       # Vercel function: proxies current banner image
│   └── banner-click.js       # Vercel function: redirects to current click URL
├── image/
│   ├── uvid/uvid.png         # UVID company logo
│   ├── banner/banner.png     # Default banner image
│   └── socialMedia/
│       ├── linkedin.png
│       ├── youtube.png
│       └── instagram.png
└── wNew Text Document.html   # Original signature HTML sample
```

---

## 📧 How to Add Signature to Outlook

1. Open the Streamlit app → fill in your details
2. Click **"📋 Copy Signature for Outlook"**
3. Open Outlook → **File → Options → Mail → Signatures → New**
4. Give the signature a name
5. Press **Ctrl+V** to paste
6. Click **OK** and set as your default signature

> **Alternative:** Use the **⬇️ Download** button → open the `.html` file in Chrome/Edge → Select All (`Ctrl+A`) → Copy → Paste into Outlook signature editor

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Signature Generator UI | Python · Streamlit |
| Dynamic Banner API | Vercel Serverless Functions (Node.js 20) |
| Banner Config Storage | GitHub raw file (`banner_config.json`) |
| Email Compatibility | Inline HTML/CSS · PNG images |
