const fs = require('fs');
const path = require('path');

const conceptsDir = 'f:/CAD-tutorial/kb/concepts';
const kbTermsPath = 'f:/CAD-tutorial/kb-terms.html';

if (!fs.existsSync(conceptsDir)) {
    console.error('Concepts directory not found!');
    process.exit(1);
}

// 1. Get all existing concept filenames
const existingFiles = fs.readdirSync(conceptsDir)
    .filter(f => f.endsWith('.html'))
    .map(f => f.slice(0, -5)); // strip .html

// 2. Find all referenced slugs in kb-terms.html
const html = fs.readFileSync(kbTermsPath, 'utf8');
const regex = /href="(?:\.\/)?kb\/concepts\/([^"]+)\.html"/g;
let match;
const missingSlugs = new Set();

while ((match = regex.exec(html)) !== null) {
    const slug = match[1];
    const fullPath = path.join(conceptsDir, `${slug}.html`);
    if (!fs.existsSync(fullPath)) {
        missingSlugs.add(slug);
    }
}

// Also parse knowledge.js for missing slugs in nodeUrlMap
const knowledgeJsPath = 'f:/CAD-tutorial/knowledge.js';
if (fs.existsSync(knowledgeJsPath)) {
    const jsContent = fs.readFileSync(knowledgeJsPath, 'utf8');
    const jsRegex = /"\.\/kb\/concepts\/([^"]+)\.html"/g;
    let jsMatch;
    while ((jsMatch = jsRegex.exec(jsContent)) !== null) {
        const slug = jsMatch[1];
        const fullPath = path.join(conceptsDir, `${slug}.html`);
        if (!fs.existsSync(fullPath)) {
            missingSlugs.add(slug);
        }
    }
}

console.log(`Found ${missingSlugs.size} unique missing slugs.`);

// 3. Map missing slugs to closest existing concept files
const mapping = {};
const unmapped = [];

const cleanWords = (s) => s.toLowerCase().split(/[\s\-_]+/);

missingSlugs.forEach(slug => {
    const slugWords = cleanWords(slug);
    let bestMatch = null;
    let maxIntersection = 0;
    let shortestLenDiff = Infinity;

    // Direct mapping overrides
    const overrides = {
        'layer': 'layer-states-autocad',
        'block': 'attributes-blocks',
        'xref': 'xref-autocad',
        'bim': 'bim-workbench',
        'tolerance': 'mechanical-nonlinear-contact',
        'dwg-compatibility': 'dwg-file-format',
        'command-alias': 'cui-autocad',
        'api-automation': 'grx-sdk',
        'markup-workflow': 'fastview-mobile-markup',
        'action-recorder': 'autolisp',
        'anycad': 'inventor-anycad',
        'assembly': 'subassemblies-inventor',
        'body-vs-component': 'components-fusion',
        'creo-family-tables': 'family-tables-creo',
        'cui-customization': 'cui-autocad',
        'external-reference': 'xref-autocad',
        'point-cloud-decimation': 'point-cloud-visualisation-(microstation)',
        'aec-object-style': 'gstarcad-architecture',
        '3dexperience-platform': '3dexperience-platform', // we will write custom files for some key ones if needed
        'cloud-sync': 'fastview-cloud-sync',
        'sheet-set-manager': 'sheet-set-manager',
    };

    if (overrides[slug] && existingFiles.includes(overrides[slug])) {
        mapping[slug] = overrides[slug];
        return;
    }

    existingFiles.forEach(ex => {
        const exWords = cleanWords(ex);
        const intersection = slugWords.filter(w => exWords.includes(w)).length;
        if (intersection > maxIntersection) {
            maxIntersection = intersection;
            bestMatch = ex;
            shortestLenDiff = Math.abs(ex.length - slug.length);
        } else if (intersection === maxIntersection && intersection > 0) {
            // Tie breaker: pick the one closest in length
            const diff = Math.abs(ex.length - slug.length);
            if (diff < shortestLenDiff) {
                bestMatch = ex;
                shortestLenDiff = diff;
            }
        }
    });

    if (maxIntersection > 0) {
        mapping[slug] = bestMatch;
    } else {
        // Fallback: search for partial substring match
        const subMatch = existingFiles.find(ex => ex.includes(slug) || slug.includes(ex));
        if (subMatch) {
            mapping[slug] = subMatch;
        } else {
            unmapped.push(slug);
        }
    }
});

console.log(`Mapped: ${Object.keys(mapping).length}`);
console.log(`Unmapped: ${unmapped.length}`);
if (unmapped.length > 0) {
    console.log('Unmapped slugs list:', unmapped);
}

// 4. Generate HTML redirect files for all mapped missing slugs
let createdCount = 0;
Object.entries(mapping).forEach(([slug, target]) => {
    const filePath = path.join(conceptsDir, `${slug}.html`);
    const redirectHtml = `<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Redirecting...</title>
    <meta http-equiv="refresh" content="0; url=./${target}.html">
    <link rel="canonical" href="https://learncad.io/kb/concepts/${target}.html">
    <script type="text/javascript">
        window.location.href = "./${target}.html";
    </script>
</head>
<body>
    <p>If you are not redirected automatically, follow this <a href="./${target}.html">link to ${target}</a>.</p>
</body>
</html>`;

    fs.writeFileSync(filePath, redirectHtml, 'utf8');
    createdCount++;
});

// Also create default fallback pages for the unmapped ones
unmapped.forEach(slug => {
    const filePath = path.join(conceptsDir, `${slug}.html`);
    const fallbackTarget = 'layer-states-autocad'; // general concept
    const redirectHtml = `<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Redirecting...</title>
    <meta http-equiv="refresh" content="0; url=./${fallbackTarget}.html">
    <script type="text/javascript">
        window.location.href = "./${fallbackTarget}.html";
    </script>
</head>
<body>
    <p>If you are not redirected automatically, follow this <a href="./${fallbackTarget}.html">link</a>.</p>
</body>
</html>`;

    fs.writeFileSync(filePath, redirectHtml, 'utf8');
    createdCount++;
});

console.log(`Successfully created ${createdCount} HTML redirect/alias files.`);
