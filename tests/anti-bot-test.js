// Unit test to verify GA4 headless bot precision detection logic
const assert = require('assert');

function runGa4Detection({ userAgent = '', webdriver = false, screen = { width: 1920, height: 1080 }, glRenderer = 'NVIDIA GeForce RTX 4070' }) {
  const window = {
    dataLayer: [],
    screen: screen,
  };
  const navigator = {
    userAgent: userAgent,
    webdriver: webdriver,
  };
  let configCalled = false;
  let configArgs = null;
  function gtag(...args) {
    window.dataLayer.push(args);
    if (args[0] === 'config') {
      configCalled = true;
      configArgs = args;
    }
  }
  window.gtag = gtag;

  const document = {
    createElement(tag) {
      if (tag === 'canvas') {
        return {
          getContext(ctx) {
            if (ctx === 'webgl' || ctx === 'experimental-webgl') {
              return {
                getExtension(name) {
                  if (name === 'WEBGL_debug_renderer_info') {
                    return { UNMASKED_RENDERER_WEBGL: 0x9246 };
                  }
                  return null;
                },
                getParameter(pname) {
                  if (pname === 0x9246) return glRenderer;
                  return '';
                }
              };
            }
            return null;
          }
        };
      }
      return {};
    }
  };

  // Run the detection snippet
  (function() {
    var gaId = 'G-ZV3YR72933';
    if (window['ga-disable-' + gaId] === true) return;
    try {
      var ua = navigator.userAgent || '';
      if (navigator.webdriver === true) {
        window['ga-disable-' + gaId] = true;
        return;
      }
      if (/HeadlessChrome|PhantomJS|Playwright|Puppeteer|SlimerJS|CasperJS/i.test(ua)) {
        window['ga-disable-' + gaId] = true;
        return;
      }
      var sw = window.screen ? window.screen.width : 0;
      var sh = window.screen ? window.screen.height : 0;
      var res = sw + 'x' + sh;
      var botRes = {
        '1280x1200': 1,
        '1366x1366': 1,
        '1280x1280': 1,
        '1600x1600': 1,
        '1280x1600': 1,
        '1600x1200': 1,
        '800x600': 1
      };
      if (botRes[res] === 1 || (sw > 0 && sw === sh)) {
        window['ga-disable-' + gaId] = true;
        return;
      }
      var canvas = document.createElement('canvas');
      var gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
      if (gl) {
        var debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
        if (debugInfo) {
          var renderer = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) || '';
          if (/SwiftShader|llvmpipe|Software Rasterizer/i.test(renderer)) {
            window['ga-disable-' + gaId] = true;
            return;
          }
        }
      }
    } catch (e) {}
    gtag('consent', 'default', {
      'analytics_storage': 'denied', 'ad_storage': 'denied', 'ad_user_data': 'denied', 'ad_personalization': 'denied',
      'region': ['AT','BE','BG','HR','CY','CZ','DK','EE','FI','FR','DE','GR','HU','IE','IT','LV','LT','LU','MT','NL','PL','PT','RO','SK','SI','ES','SE','IS','LI','NO','GB','CH'],
      'wait_for_update': 500
    });
    gtag('consent', 'default', {
      'analytics_storage': 'granted', 'ad_storage': 'denied', 'ad_user_data': 'denied', 'ad_personalization': 'denied'
    });
    gtag('js', new Date());
    gtag('config', gaId);
  })();

  return {
    disabled: window['ga-disable-G-ZV3YR72933'] === true,
    configCalled: configCalled,
    configArgs: configArgs
  };
}

// Test cases
console.log('--- Running GA4 Anti-Bot Detection Tests ---');

// 1. Legitimate user on desktop
{
  const res = runGa4Detection({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    webdriver: false,
    screen: { width: 1920, height: 1080 },
    glRenderer: 'ANGLE (NVIDIA, NVIDIA GeForce RTX 3080 Direct3D11 vs_5_0 ps_5_0)'
  });
  assert.strictEqual(res.disabled, false, 'Legitimate user should NOT be disabled');
  assert.strictEqual(res.configCalled, true, 'gtag config should be called for legitimate user');
  console.log('PASS: Legitimate user runs 0ms normally');
}

// 2. Headless webdriver = true
{
  const res = runGa4Detection({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    webdriver: true,
    screen: { width: 1920, height: 1080 }
  });
  assert.strictEqual(res.disabled, true, 'webdriver=true must disable GA');
  assert.strictEqual(res.configCalled, false, 'gtag config must NOT be called for webdriver=true');
  console.log('PASS: navigator.webdriver === true intercepted');
}

// 3. UserAgent HeadlessChrome
{
  const res = runGa4Detection({
    userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/125.0.0.0 Safari/537.36',
    webdriver: false,
    screen: { width: 1920, height: 1080 }
  });
  assert.strictEqual(res.disabled, true, 'HeadlessChrome must disable GA');
  assert.strictEqual(res.configCalled, false, 'gtag config must NOT be called');
  console.log('PASS: HeadlessChrome UA intercepted');
}

// 4. UserAgent Playwright / Puppeteer
{
  const res = runGa4Detection({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Puppeteer/22.0.0 Safari/537.36',
    webdriver: false,
    screen: { width: 1920, height: 1080 }
  });
  assert.strictEqual(res.disabled, true, 'Puppeteer must disable GA');
  assert.strictEqual(res.configCalled, false, 'gtag config must NOT be called');
  console.log('PASS: Puppeteer UA intercepted');
}

// 5. Datacenter resolution 1280x1200
{
  const res = runGa4Detection({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    webdriver: false,
    screen: { width: 1280, height: 1200 }
  });
  assert.strictEqual(res.disabled, true, '1280x1200 container resolution must disable GA');
  assert.strictEqual(res.configCalled, false, 'gtag config must NOT be called');
  console.log('PASS: 1280x1200 virtual container resolution intercepted');
}

// 6. Datacenter resolution square screen (e.g. 1000x1000)
{
  const res = runGa4Detection({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    webdriver: false,
    screen: { width: 1000, height: 1000 }
  });
  assert.strictEqual(res.disabled, true, 'Square virtual screen must disable GA');
  assert.strictEqual(res.configCalled, false, 'gtag config must NOT be called');
  console.log('PASS: Square screen (sw === sh) intercepted');
}

// 7. WebGL SwiftShader CPU software renderer
{
  const res = runGa4Detection({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    webdriver: false,
    screen: { width: 1920, height: 1080 },
    glRenderer: 'Google SwiftShader'
  });
  assert.strictEqual(res.disabled, true, 'SwiftShader WebGL renderer must disable GA');
  assert.strictEqual(res.configCalled, false, 'gtag config must NOT be called');
  console.log('PASS: SwiftShader CPU renderer intercepted');
}

// 8. WebGL llvmpipe CPU software renderer
{
  const res = runGa4Detection({
    userAgent: 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0',
    webdriver: false,
    screen: { width: 1920, height: 1080 },
    glRenderer: 'llvmpipe (LLVM 15.0.7, 256 bits)'
  });
  assert.strictEqual(res.disabled, true, 'llvmpipe WebGL renderer must disable GA');
  assert.strictEqual(res.configCalled, false, 'gtag config must NOT be called');
  console.log('PASS: llvmpipe CPU software rasterizer intercepted');
}

console.log('✅ ALL GA4 ANTI-BOT TESTS PASSED!');
