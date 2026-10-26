/**
 * Cloudflare Pages Edge Middleware (functions/_middleware.js)
 *
 * Uses Cloudflare's built-in streaming HTMLRewriter to automatically inject
 * `data-cfasync="false"` into all executable <script> tags across the site.
 * This prevents Cloudflare Rocket Loader from rewriting scripts into
 * `type="...-text/javascript"` and blocking GA4 telemetry or UI interactivity.
 */

class ScriptRocketLoaderBypassHandler {
  element(element) {
    const type = (element.getAttribute('type') || '').toLowerCase().trim();
    // Do not touch JSON-LD structured data blocks
    if (type === 'application/ld+json') {
      return;
    }
    if (!element.hasAttribute('data-cfasync')) {
      element.setAttribute('data-cfasync', 'false');
    }
  }
}

export async function onRequest(context) {
  const response = await context.next();
  const contentType = response.headers.get('content-type') || '';

  if (contentType.includes('text/html')) {
    return new HTMLRewriter()
      .on('script', new ScriptRocketLoaderBypassHandler())
      .transform(response);
  }

  return response;
}
