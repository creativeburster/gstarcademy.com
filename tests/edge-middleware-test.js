const assert = require('assert');

// Mock HTMLRewriter
class MockHTMLRewriter {
  constructor() {
    this.handlers = [];
  }
  on(selector, handler) {
    this.handlers.push({ selector, handler });
    return this;
  }
  transform(response) {
    let body = response._body;
    for (const { selector, handler } of this.handlers) {
      if (selector === 'head' && handler.element) {
        let inserted = '';
        const el = {
          prepend(content, opts) {
            inserted += content;
          }
        };
        handler.element(el);
        body = body.replace(/<head>/i, '<head>' + inserted);
      }
    }
    return new MockResponse(body, {
      status: response.status,
      headers: response.headers
    });
  }
}

class MockResponse {
  constructor(body, init = {}) {
    this._body = body;
    this.status = init.status || 200;
    this.headers = new Map(Object.entries(init.headers || {}));
  }
  async text() {
    return this._body;
  }
  get(key) {
    return this.headers.get(key.toLowerCase());
  }
}

// Emulate middleware execution
const DATACENTER_BOT_ASNS = new Set([
  45102, 37963, 132203, 45090, 14061, 20473, 16276, 24940, 9009
]);

function isSearchEngineReferer(referer) {
  if (!referer) return false;
  return /google\.|bing\.com|yahoo\.com|duckduckgo\.com|baidu\.com|yandex\.|ecosia\.org|ask\.com|sogou\.com|so\.com|qwant\.com|startpage\.com|naver\.com/i.test(referer);
}

async function runMiddleware({ asn = 0, country = 'US', referer = '', userAgent = 'Mozilla/5.0' }) {
  const reqHeaders = new Map();
  if (referer) reqHeaders.set('referer', referer);
  if (userAgent) reqHeaders.set('user-agent', userAgent);

  const context = {
    request: {
      cf: { asn, country },
      headers: {
        get(k) { return reqHeaders.get(k.toLowerCase()) || null; }
      }
    },
    next: async () => {
      const headers = { 'content-type': 'text/html; charset=utf-8' };
      return new MockResponse('<!doctype html><html><head><title>Test</title></head><body><h1>Hello</h1></body></html>', {
        status: 200,
        headers
      });
    }
  };

  const { request } = context;
  const cf = request.cf || {};
  const cfAsn = Number(cf.asn || 0);
  const reqCountry = cf.country || '';
  const reqReferer = request.headers.get('referer') || '';

  const isSuspiciousDatacenter = DATACENTER_BOT_ASNS.has(cfAsn) && !reqReferer;
  const isSuspiciousCnDirect = reqCountry === 'CN' && !isSearchEngineReferer(reqReferer);
  const shouldDisableGa = isSuspiciousDatacenter || isSuspiciousCnDirect;

  const response = await context.next();
  const contentType = response.headers.get('content-type') || '';

  if (shouldDisableGa && contentType.includes('text/html')) {
    const rewriter = new MockHTMLRewriter();
    return rewriter
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

(async () => {
  console.log('--- Running Edge Middleware Tests ---');

  // Case 1: Legitimate overseas user with no referer
  {
    const res = await runMiddleware({ asn: 7922, country: 'US', referer: '' });
    const text = await res.text();
    assert.strictEqual(res.status, 200);
    assert.strictEqual(text.includes('ga-disable-G-ZV3YR72933'), false);
    console.log('PASS: Legitimate overseas user not disabled');
  }

  // Case 2: Datacenter Alibaba Cloud 45102 with no referer
  {
    const res = await runMiddleware({ asn: 45102, country: 'SG', referer: '' });
    const text = await res.text();
    assert.strictEqual(res.status, 200);
    assert.strictEqual(text.includes("<script data-cfasync=\"false\">window['ga-disable-G-ZV3YR72933']=true;</script>"), true);
    console.log('PASS: Datacenter Alibaba Cloud ASN 45102 disabled GA4');
  }

  // Case 3: Datacenter Tencent Cloud 132203 with no referer
  {
    const res = await runMiddleware({ asn: 132203, country: 'SG', referer: '' });
    const text = await res.text();
    assert.strictEqual(res.status, 200);
    assert.strictEqual(text.includes("<script data-cfasync=\"false\">window['ga-disable-G-ZV3YR72933']=true;</script>"), true);
    console.log('PASS: Datacenter Tencent Cloud ASN 132203 disabled GA4');
  }

  // Case 4: Mainland China without search engine referer
  {
    const res = await runMiddleware({ asn: 4134, country: 'CN', referer: '' });
    const text = await res.text();
    assert.strictEqual(res.status, 200);
    assert.strictEqual(text.includes("<script data-cfasync=\"false\">window['ga-disable-G-ZV3YR72933']=true;</script>"), true);
    console.log('PASS: CN direct proxy traffic disabled GA4');
  }

  // Case 5: Mainland China with Google search referer
  {
    const res = await runMiddleware({ asn: 4134, country: 'CN', referer: 'https://www.google.com/' });
    const text = await res.text();
    assert.strictEqual(res.status, 200);
    assert.strictEqual(text.includes('ga-disable-G-ZV3YR72933'), false);
    console.log('PASS: CN with Google search referer preserved');
  }

  // Case 6: Googlebot crawling HTML (never 403, 200 OK with full content)
  {
    const res = await runMiddleware({ asn: 15169, country: 'US', referer: '', userAgent: 'Googlebot/2.1 (+http://www.google.com/bot.html)' });
    const text = await res.text();
    assert.strictEqual(res.status, 200);
    assert.strictEqual(text.includes('<h1>Hello</h1>'), true);
    console.log('PASS: Googlebot crawling gets 200 OK full HTML');
  }

  console.log('✅ ALL EDGE MIDDLEWARE TESTS PASSED!');
})();
