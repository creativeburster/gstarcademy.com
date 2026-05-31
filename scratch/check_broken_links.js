const fs = require('fs');
const path = require('path');

const kbTermsPath = 'f:/CAD-tutorial/kb-terms.html';
const conceptsDir = 'f:/CAD-tutorial/kb/concepts';

if (!fs.existsSync(kbTermsPath)) {
    console.error('kb-terms.html not found!');
    process.exit(1);
}

const html = fs.readFileSync(kbTermsPath, 'utf8');

// Find all href="./kb/concepts/*.html" or href="kb/concepts/*.html"
const regex = /href="(?:\.\/)?kb\/concepts\/([^"]+)\.html"/g;
let match;
const missing = new Set();
const total = new Set();

while ((match = regex.exec(html)) !== null) {
    const slug = match[1];
    total.add(slug);
    const fullPath = path.join(conceptsDir, `${slug}.html`);
    if (!fs.existsSync(fullPath)) {
        missing.add(slug);
    }
}

console.log(`Total unique concept links in kb-terms.html: ${total.size}`);
console.log(`Missing/404 concept files: ${missing.size}`);
console.log('List of missing slugs:');
console.log(Array.from(missing).sort());
