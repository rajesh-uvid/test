/**
 * /api/banner-image
 *
 * Called as the `src` of the banner <img> in the email signature.
 * Every time an email is opened, this function:
 *   1. Reads banner_config.json from GitHub (always fresh)
 *   2. Fetches the actual image from the URL in the config
 *   3. Streams the image bytes back with no-cache headers
 *
 * Result: Change banner_config.json → push to GitHub →
 *         next email open shows the new banner automatically.
 */

const CONFIG_URL =
  "https://raw.githubusercontent.com/rajesh-uvid/test/refs/heads/main/banner_config.json";

const FALLBACK_IMAGE =
  "https://raw.githubusercontent.com/rajesh-uvid/test/refs/heads/main/image/banner/banner.png";

export default async function handler(req, res) {
  let imageUrl = FALLBACK_IMAGE;

  try {
    // Always fetch fresh — no caching here
    const configRes = await fetch(CONFIG_URL, {
      headers: { "Cache-Control": "no-cache" },
    });
    if (configRes.ok) {
      const config = await configRes.json();
      imageUrl = config.banner_image_url || FALLBACK_IMAGE;
    }
  } catch (_) {
    // Use fallback silently
  }

  try {
    const imageRes = await fetch(imageUrl);
    if (!imageRes.ok) throw new Error("Image fetch failed");

    const contentType =
      imageRes.headers.get("content-type") || "image/png";
    const buffer = await imageRes.arrayBuffer();

    // Prevent ALL caching so every email open re-fetches
    res.setHeader("Content-Type", contentType);
    res.setHeader("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0");
    res.setHeader("Pragma", "no-cache");
    res.setHeader("Expires", "0");
    res.setHeader("Surrogate-Control", "no-store");
    res.status(200).send(Buffer.from(buffer));
  } catch (err) {
    res.status(302).redirect(FALLBACK_IMAGE);
  }
}
