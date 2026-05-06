# CAD Learn Hub - DESIGN.md

## Design Intent

Create a premium, modern, and long-term friendly interface for a CAD tutorial navigation website.
The style should feel trustworthy and efficient (Stripe-like clarity) with refined visual depth and polish (Linear-like precision), while staying beginner-friendly.

Primary UX goals:

1. Make first impression "high-end and clear"
2. Reduce visual fatigue for returning visitors
3. Keep readability and information hierarchy strong for SEO content pages
4. Preserve fast loading and low visual noise

## Visual Style

- Primary style (A plan): `Linear-inspired minimal premium`
- Style blend: `clean monochrome base + restrained indigo accents + subtle depth`
- Tone: `professional`, `technical`, `calm`, `future-ready`
- Avoid: over-bright neon, heavy skeuomorphic effects, noisy backgrounds

## Color System

- Primary: `#4F46E5`
- Secondary: `#0EA5E9`
- Accent: `#06B6D4`
- Text (light): `#101829`
- Muted text (light): `#5C6882`
- Surface (light): `#FFFFFF` with slight gradient
- Border (light): `#DBE3F0`

Dark mode (auto via `prefers-color-scheme`):

- Background: `#070B13`
- Surface: `#111B2F`
- Border: `#25324B`
- Text: `#D8E3F8`
- Muted text: `#93A5C4`

## Typography

- Font stack: `Inter, Segoe UI, SF Pro Display, Roboto, Arial, sans-serif`
- Body base: `16px`
- Body line-height: `1.6+`
- Heading style: high contrast, compact line-height, balanced wrapping
- Keep content readable for long-form SEO pages

## Spacing and Radius

- Spacing rhythm: `4 / 8 / 12 / 16 / 24 / 32 / 40`
- Card radius: `18px`
- Small radius: `12px`
- Hero radius: `28px`

## Shadows and Depth

- Default shadow: soft and diffused for cards and panels
- Elevated shadow: stronger for hero and key containers
- Hover interaction: slight lift (`translateY(-1px to -2px)`) + stronger shadow

## Components

### Navigation

- Pill-like nav links
- Active state uses subtle gradient tint and inner border
- Sticky blurred top bar

### Hero

- Premium gradient mesh background with clean headline
- Large title with strong contrast
- Secondary visual card can use gradient + translucent stat cells

### Cards and Panels

- Light gradient surfaces, crisp borders, soft shadows
- Hover should feel responsive but not jumpy

### Buttons

- Primary: gradient fill (`primary -> secondary`) and glow shadow
- Secondary: neutral surface with soft hover lift

### Tags/Chips

- Rounded pills, low-contrast background, clear text
- Active tags show stronger border and tinted background

## Motion

- Micro-interactions only
- Duration range: `150-250ms`
- Use transform and opacity
- Respect reduced motion preferences

## Accessibility

- Maintain strong text contrast in light and dark modes
- Preserve clear focus/hover/active states
- Keep touch/click targets comfortably sized
- Avoid color-only meaning where possible

## SEO + Performance Guardrails

- Do not add heavy JS animations to content pages
- Keep decorative effects in CSS, not large runtime scripts
- Reuse shared components and tokens
- Prioritize fast first paint and stable layout

## Implementation Rule for AI tools

When generating or modifying UI, follow this file as the source of truth.
Do not introduce a different visual language per page.
Keep all pages in one coherent system: same color tokens, spacing scale, radius scale, shadow scale, and interaction timing.
