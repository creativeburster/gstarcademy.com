/**
 * Cloudflare Pages Middleware: Edge Layer Anti-Bot & GA4 Shield
 * 
 * 1. Blocks fake traffic from known datacenter ASNs and headless crawlers without referrers
 *    by disabling GA4 tracking at the edge before client JS execution.
 * 2. Shields GA4 against mainland China (CN) proxy pools & automated scrapers
 *    (e.g., Chrome v151 / 375x667 mobile crawlers) for pure overseas English audience.
 * 3. Never blocks HTML body or returns 403/4xx to ensure legitimate search engine crawlers
 *    (Googlebot, Bingbot) and AI web agents (ChatGPT, Claude, Perplexity) crawl 100% unaffected.
 */

const DATACENTER_BOT_ASNS = new Set([
  45102,  // Alibaba Cloud (Singapore / US)
  37963,  // Alibaba Cloud
  132203, // Tencent Cloud (Singapore)
  45090,  // Tencent Cloud
  14061,  // DigitalOcean
  20473,  // Vultr / Choopa
  16276,  // OVH
  24940,  // Hetzner
  9009,   // M247
]);

function isSearchEngineReferer(referer) {
  if (!referer) return false;
  return /google\.|bing\.com|yahoo\.com|duckduckgo\.com|baidu\.com|yandex\.|ecosia\.org|ask\.com|sogou\.com|so\.com|qwant\.com|startpage\.com|naver\.com/i.test(referer);
}

export async function onRequest(context) {
  const { request } = context;
  const cf = request.cf || {};
  const cfAsn = Number(cf.asn || 0);
  const country = cf.country || '';
  const referer = request.headers.get('referer') || '';

  // 1. 已知云机房 ASN 且无 Referer
  const isSuspiciousDatacenter = DATACENTER_BOT_ASNS.has(cfAsn) && !referer;

  // 2. 本站是面向全球的纯英文知识库（不做中国大陆市场），如果来自中国大陆（CN）且无搜索引擎 Referer，
  // 同样在前端设置 window['ga-disable-G-ZV3YR72933'] = true，防止国内代理池 Chrome v151 / 375x667 爬虫污染 GA4 统计
  const isSuspiciousCnDirect = country === 'CN' && !isSearchEngineReferer(referer);

  const shouldDisableGa = isSuspiciousDatacenter || isSuspiciousCnDirect;

  const response = await context.next();
  const contentType = response.headers.get('content-type') || '';

  // 仅在 HTML 响应且命中机房/代理特征时，在 <head> 最顶部注入 GA4 熔断代码
  // 保持 200 OK 正常响应，绝不误伤搜索引擎和 AI 爬虫抓取网页 HTML 内容
  if (shouldDisableGa && contentType.includes('text/html') && typeof HTMLRewriter !== 'undefined') {
    return new HTMLRewriter()
      .on('head', {
        element(el) {
          el.prepend(
            `<script data-cfasync="false">window['ga-disable-G-ZV3YR72933']=true;</script>`,
            { html: true }
          );
        }
      })
      .transform(response);
  }

  return response;
}
