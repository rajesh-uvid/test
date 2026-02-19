/**
 * /api/banner-click
 *
 * Called as the `href` when someone clicks the banner in their email.
 * Reads banner_config.json from GitHub and 302-redirects to the
 * current target URL — so you can change the destination anytime.
 *
 * Usage: set banner <a href="https://your-app.vercel.app/api/banner-click">
 */

const CONFIG_URL =
    "https://raw.githubusercontent.com/rajesh-uvid/test/refs/heads/main/banner_config.json";

const FALLBACK_LINK = "https://www.uvidconsulting.com";

export default async function handler(req, res) {
    let linkUrl = FALLBACK_LINK;

    try {
        const configRes = await fetch(CONFIG_URL, {
            headers: { "Cache-Control": "no-cache" },
        });
        if (configRes.ok) {
            const config = await configRes.json();
            linkUrl = config.banner_link_url || FALLBACK_LINK;
        }
    } catch (_) {
        // Use fallback silently
    }

    // No-cache + 302 redirect to current destination
    res.setHeader("Cache-Control", "no-cache, no-store, must-revalidate");
    res.setHeader("Pragma", "no-cache");
    res.redirect(302, linkUrl);
}
