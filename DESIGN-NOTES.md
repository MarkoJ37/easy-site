# DESIGN-NOTES.md — easy.rs

## Decision — 23 October 2026, later the same day (Marko): hero image restored

The single-column hero below is **reversed**. Current state:

- **Hero = two columns from `lg`:** copy left, the conceptual IT still life right
  (laptop, monitor, switch, NAS on white). Below `lg` the image stacks under the copy on
  the same left edge — never centred under left-aligned text.
- **The image's screens are flat and off:** a single neutral graphite, no decorative
  wallpaper. The glossy blue-wave wallpaper was the main AI-stock tell; it was painted out
  of the existing render (no regeneration was available). Bezels, devices and light are
  untouched. This is a deliberate exception to §6.1's "no hero art", made by Marko.
- **Caption bar:** status dot + `easy.rs` only. The invented tagline stays removed
  (CLAUDE.md §0).
- **Unchanged from the block below:** the four facts live only in the TrustBar (§6b.3),
  motion is exactly §7, Space Grotesk scope, the button scale, and `og.jpg` stays the logo
  card.
- **Terminology:** the lead magnet is **"konsultacija"** everywhere (see CLAUDE.md §0).

## Decision — 23 October 2026 (Marko): hero contradiction resolved

> **Hero part SUPERSEDED** by the block above (single column → two columns with the
> flat-screen image). Every other point here still applies.

This file had contradicted itself on the hero. Resolved in favour of the original
intent (§5/§6), with one change:

- **Hero = single column.** Eyebrow with pulse dot / H1 / sub / two CTAs, left-aligned.
  No right-column object of any kind — no image, no diagram, no facts panel.
- **The four facts live only in the TrustBar** directly under the hero (§6b.3 kept).
- **No hero art, ever** (§6.1 stands). The generated still life and its web/OG assets
  are deleted. `public/og.jpg` is now the real logo, one-colour white, on `--ink`,
  built by `node scripts/build-og.mjs` — no re-typeset wordmark, no extra copy.
- **Motion is exactly §7:** scroll reveal, hero dot pulse, nav shadow. Hover changes
  colour only — no lifts, no shadows on cards. The FAQ chevron rotation (§5) stays.
- **Space Grotesk in its four places only** (§3): H1, H2, prices, the Win10 heading — plus
  the two spots §5 names explicitly (the O nama "1999." figure and the shop card brand field).
- **Buttons:** one scale in `global.css` (`.btn`, `.btn-sm`), Plex 600.

Superseded and kept below only as history: the 11 Sept hero-image paragraph, §6b.2, and
the §6b motion-budget addition. The §5 wireframe's right-column hero panel is replaced
by the single column above.

## Revision — 11 September 2026

> **SUPERSEDED (23 Oct 2026)** as far as the hero and social image go — see the decision
> above. The catalog, font and verification notes in this block still apply.

The user requested replacement visuals and a full visual review. The hero now pairs
the original headline with a custom, cool-neutral 3D IT still life in the existing navy,
blue and green palette. The composition is conceptual, not a company/product photograph.
An accompanying 1200×630 social card uses the same visual direction. Source prompts
and artwork are in `artwork/`; optimized web assets are in `public/`.

The catalog retains honest typographic product cards, with category labels, 12-item
pagination, horizontal category filters and explicit quote-time availability.
The logo, section order and core palette remain. Fonts are now served locally with
Serbian Latin coverage. Browser review covers 360/768/1440px, focus, motion, contrast,
form errors and sticky offsets. Screenshots: `artifacts/visual/`.

Earlier sketches and open-item lists below are historical; current setup is in README.md.

Pass 1 (plan) and pass 2 (self-critique) per CLAUDE.md §2. **No code written yet.**
Every visual decision in the build must trace back to a token in §2 or a rule in §5 of this file.

---

## 1. What the existing logo forces

`logo/logo.png` — 500×500, transparent background, raster. Colors sampled directly from the file:

| Role in the lockup | Sampled hex | Notes |
|---|---|---|
| Rounded square + "easy" wordmark | **`#0F2C4E`** | dominant color, 1000+ px at the sample rate |
| "computers" subline | **≈ `#1E76A6`** | small anti-aliased text — no pixel reaches full saturation, so this is the darkest stroke core, not a certain value |

CLAUDE.md §2 cites `#17334A` / `#2F9FDB` from the ponuda template. **The actual file is deeper and less cyan than both.** Tokens below follow the file, not the remembered values — and the accent gets re-sampled the moment we have a vector.

Three consequences:

1. **The logo is raster and must be vectorized before nav/favicon work.** At nav size (~150px wide) a 500px PNG is passable at 1x and soft at 2x; a favicon traced from it will be mush. Path: Inkscape trace or vectorizer.ai on the mark, then rebuild the two text runs as outlines.
2. **The lockup's typeface is neither Space Grotesk nor IBM Plex.** "easy" reads as a humanist face with visible stress; "computers" is a light letterspaced sans. That is fine — the lockup ships as an SVG image and is never re-typeset in CSS. But it means the wordmark can't be reproduced in markup, so the nav logo is an inline SVG, not styled text.
3. **Navy plus mid-blue is the single most generic Serbian IT palette there is** (every hosting company, every servis, every ISP). The logo is fixed, so the plan below deliberately does *not* try to out-color it — see §6.

---

## 2. Palette (proposed token overrides)

CLAUDE.md §2 authorizes shifting `--ink`/`--accent` toward the logo. It does not authorize the paper change — **that one is a proposal for Marko**, marked below.

```css
:root {
  --ink:        #0F2C4E;  /* logo navy — headings, body text, nav, footer, inverted cards */
  --paper:      #F7F8F9;  /* PROPOSED override of #FAFAF7 (see note) */
  --surface:    #FFFFFF;  /* cards sitting on paper */
  --steel:      #5A6675;  /* secondary text, meta, hairlines (blue-cast neutral) */
  --line:       #E3E7EB;  /* 1px rules, card borders */
  --accent:     #1A6C99;  /* links + primary CTA — logo blue, darkened to clear AA */
  --signal:     #17A34A;  /* THE status dot. Graphic use only */
  --signal-ink: #10763A;  /* the same green when it has to be readable text */
}
```

**Contrast, all against `--paper`, all measured not guessed:**

| Pair | Ratio | Verdict |
|---|---|---|
| `--ink` on `--paper` | **12.7 : 1** | AAA |
| `--steel` on `--paper` | **5.5 : 1** | AA body, AAA large |
| `--accent` on `--paper` | **5.2 : 1** | AA body |
| `--signal` on `--paper` | **3.0 : 1** | fails for text — dot/border/icon only |
| `--signal-ink` on `--paper` | **5.2 : 1** | AA body — use for "Na stanju" and any green *word* |
| `#FFFFFF` on `--ink` | **13.9 : 1** | AAA — the inverted card and Win10 strip are safe |
| `--signal` on `--ink` | **4.2 : 1** | large text / graphic only — never small green text on navy |

**Why paper moves from `#FAFAF7` to `#F7F8F9`:** `#FAFAF7` is a warm off-white (yellow-leaning). Under a `#0F2C4E` navy it reads slightly dirty — the classic cream-under-navy mismatch. `#F7F8F9` is the same lightness, cool-neutral, and lets the navy sit clean. If Marko prefers the original it still passes every contrast check above; this is taste, not accessibility.

**The cobalt `#2450E6` from the starting tokens is dropped.** It is a different hue family from the logo's blue and the two together look like an accident. One blue, taken from the logo.

---

## 3. Type scale

Space Grotesk (display, 500/700) + IBM Plex Sans (body, 400/600), Google Fonts, `latin-ext` subset.

| Role | Family / weight | Size | Line-height | Tracking |
|---|---|---|---|---|
| H1 | Space Grotesk 700 | `clamp(2.15rem, 1.35rem + 3.4vw, 3.4rem)` | 1.05 | −0.02em |
| H2 (section) | Space Grotesk 500 | `clamp(1.6rem, 1.2rem + 1.6vw, 2.2rem)` | 1.15 | −0.01em |
| H3 (card title) | IBM Plex Sans 600 | 1.0625rem | 1.35 | 0 |
| Body | IBM Plex Sans 400 | 1.0625rem (17px) | 1.6 | 0 |
| Lead / hero sub | IBM Plex Sans 400 | 1.1875rem | 1.55 | 0 |
| Small / meta / "sa PDV-om" | IBM Plex Sans 400 | 0.875rem | 1.45 | 0 |
| Eyebrow / label | IBM Plex Sans 600 | 0.75rem uppercase | 1.2 | +0.08em |
| Price | Space Grotesk 500, `tabular-nums` | 1.5–2rem | 1.1 | −0.01em |

Space Grotesk appears in exactly four places: H1, section H2s, prices, and the Win10 date. Everything else is Plex. Display type used sparingly is the brief's instruction and also the thing that keeps two-font pairings from looking like a template.

**Must verify before shipping (CLAUDE.md §8):** Space Grotesk's `latin-ext` coverage of **š đ č ć ž** at 500 *and* 700. Plex Sans is known-good. If Grotesk's ć/đ are missing or badly drawn at either weight, the fallback is Plex Sans 600 for display with tighter tracking — decided by looking, not by assuming.

---

## 4. The signature element: the status rail

The brief names the green dot as the one memorable device. A dot alone is decoration; what makes it *this site's* device is giving it something to sit on.

**The rail:** a 1px `--line` hairline running down the left edge of the section stack on desktop, with a `--signal` dot as a node at each section start. It reads as an uptime/monitoring line — honest to what the company actually sells — and it costs one border and one pseudo-element. Below 768px the rail collapses and only the dots remain, inline before each section eyebrow.

Dot appearances, in full:

- Hero eyebrow — a dot with a slow expanding ring (2.4s, opacity only). Static under `prefers-reduced-motion`.
- Rail nodes — one per section, solid, 6px.
- Paketi bullets — the dot replaces the list marker.
- Proces — the three step numbers are nodes on a short horizontal run of the same rail.
- Shop availability — dot plus text in `--signal-ink`.
- Favicon — navy rounded square from the logo mark, green dot in the corner.
- Footer — one quiet dot, `--steel`, no pulse.

That is the entire decorative budget. No gradients, no glows, no blobs, no background patterns, no icon-in-tinted-circle.

---

## 5. Layout

Container `max-width: 1100px`, gutters 20px (mobile) / 32px (≥768px). Section rhythm `padding-block: clamp(3.5rem, 8vw, 6rem)`. Radius 6px everywhere except the 8px pricing cards. Borders 1px `--line`; shadows only on the sticky nav after scroll.

```
+-- NAV (sticky, 60px, --surface, 1px bottom rule, backdrop-blur after 40px scroll)
|   [logo.svg 148px]      Usluge  Cene  Oprema  Kontakt  [ Besplatan snimak IT stanja ]
+-------------------------------------------------------------------------------------
    HERO - 2 col at >=900px (7/5), stacked below. NOT centered.
    * IT PARTNER ZA MALA PREDUZECA - BEOGRAD        |
    Racunari, mreza i licence -                     |  (right col: typographic panel,
    da jednostavno rade.                            |   navy fill, the four TrustBar
    [sub, 2 lines, --steel]                         |   facts as a stacked list with
    [ Zakazite besplatan snimak ] [Pogledajte opremu]|   hairline separators)
-------------------------------------------------------------------------------------
    TRUSTBAR - 4 facts, 1px rules between, 4-col -> 2-col -> 1-col
-------------------------------------------------------------------------------------
    USLUGE - 6 items, 3 col at >=900px / 2 col at >=600px / 1 col.
    Rule-separated, NOT boxed: 20px lucide icon in --accent, H3, 2 lines --steel.
-------------------------------------------------------------------------------------
    PAKETI #cene - 3 cards, equal size. STANDARD = navy fill + white text, same
    dimensions, no scale-up, no glow; its badge is a green dot + "najcesci izbor".
    Below: ad-hoc line, then the bez-PDV / 30-dana note in small --steel.
-------------------------------------------------------------------------------------
    WIN10 - full-bleed --ink. Date set in Space Grotesk 700 at H2 size, white.
    Body white at 82% opacity. CTA = white outline button. NO red, NO warning icon.
-------------------------------------------------------------------------------------
    PROCES - 3 steps on a horizontal rail (vertical below 768px). Numbers are nodes.
-------------------------------------------------------------------------------------
    O NAMA - single measure, max 62ch, 3 paragraphs (see §8 note). Beside it a
    typographic panel: "1999" in Space Grotesk at display size, "- i dalje isti posao"
    under it in --steel. No photo, no placeholder frame, no silhouette.
-------------------------------------------------------------------------------------
    FAQ - native <details>, 6 items, rule-separated, chevron rotates. Full-width row
    is the click target.
-------------------------------------------------------------------------------------
    KONTAKT #kontakt - 2 col at >=900px: form (7) | direct contacts + radno vreme (5).
-------------------------------------------------------------------------------------
    FOOTER - --ink fill. Legal line, Privatnost, (c) year, one quiet dot.
```

`/shop`: same nav, then a compact header, the disclaimer strip on `--surface` with a left `--accent` 2px edge, sticky filter chips plus search, then a 3/2/1-col card grid. Cards without an image get a typographic treatment — brand name in Space Grotesk on a `--paper` field — never a grey box with a broken-image icon.

---

## 6. Self-critique

Five ways this plan could have come out generic, and what each one costs.

1. **"Navy plus blue IT site" is the default.** It is, and the logo locks the hues. The escape is not a weirder palette — it is *restraint*: the page is near-monochrome navy on cool white, blue appears only on links and one CTA, and green appears only as the dot. Explicitly banned: blue gradient hero, blue-filled section bands, white icons in blue circles, hero art. If the page reads as "navy text on white with one green dot," the plan worked.
2. **Six icon cards in a 3×2 grid is the most copied section on the web.** The brief specifies cards with icon/title/two lines, so the content stays — but the *boxes* go. Rule-separated rows with small line icons say "a real firm listing what it does"; bordered cards with 48px icons say "SaaS template." This is a deviation from the word "cards" in §3.4 and is flagged for Marko rather than assumed.
3. **A scaled-up middle pricing card with a glowing badge is a SaaS tell.** STANDARD is featured by *inversion* (navy fill) at identical dimensions. Nothing scales, nothing glows.
4. **The Win10 banner wants to become a red alert strip.** Red plus a warning triangle turns a real deadline into fearmongering and undercuts the calm the rest of the page is buying. Navy field, big date, plain sentence, outline CTA.
5. **AI-default check.** Not cream+terracotta serif. Not near-black plus acid green — `#17A34A` is a true green, kept to a 6px dot and never used as a fill or as small text. Passed.

One risk this plan does **not** solve: O nama and the whole shop launch without a single photograph. The typographic panels are a real treatment, not a placeholder, but five phone photos of the radnja and magacin (plan §8 item 5) would do more for trust than anything in this document.

---

## 6b. Revision after the stage 2 review (Marko, 18 Aug)

The first build read as **basic** — restraint tipped over into unfinished. Three changes:

1. **Section eyebrows removed.** The `● Usluge` / `● Cene` / `● Kontakt` labels above every H2 were repeating the heading in smaller type. Only the hero eyebrow survives, and it drops the `— Beograd` suffix. Sections now open on the H2.
2. ~~**The hero gets a real graphic:**~~ **SUPERSEDED (23 Oct 2026)** — hero is single column, no graphic; see the decision at the top. Original text, for history: **The hero gets a real graphic:** an abstract office-network diagram — router, switch, four endpoints — drawn in navy hairlines with `--signal` dots marking live nodes and an animated dashed stroke running along the spine as traffic. This is the "sve radi" idea made visible, and it satisfies CLAUDE.md §0's *typographic/graphic treatment where no photo exists* without a single stock image. A faded dot-grid sits behind the hero for texture.
3. **The trust facts stopped being duplicated.** They were in both the hero's navy panel and the white TrustBar band, which stacked on mobile. TrustBar is now their only home at every breakpoint, and it carries the **navy** treatment Marko preferred — full-bleed `--ink` with green dots and hairline dividers, not the white band.

   This puts navy at three points in the scroll (TrustBar, Win10, footer), which gives the page its rhythm: paper → navy → white → paper → navy → white → paper → white → paper → navy.

~~Added to the motion budget (§7): the traffic dashes, the node blink, and a hover lift on the pricing cards and CTAs.~~ **SUPERSEDED (23 Oct 2026)** — §7's three items are the whole budget.

The §6 bans still hold: no gradient hero, no blue section fills, no glowing badges, no red on the Win10 strip.

---

## 7. Motion

One scroll-reveal: 12px rise plus fade, 320ms, `cubic-bezier(.2,.6,.2,1)`, `IntersectionObserver`, once per section, no stagger. The hero dot pulse. Nav shadow on scroll. Nothing else. Under `prefers-reduced-motion: reduce` all three become static — content is visible at rest, never revealed by script alone.

---

## 8. Open items before coding

- [ ] **Marko approves or rejects** the three deviations: paper `#F7F8F9`, cobalt dropped, Usluge as rules instead of boxes.
- [ ] Vectorize `logo/logo.png` into `public/logo.svg`, then re-sample the true accent blue and correct `--accent` if it differs from `#1E76A6`.
- [ ] Favicon set and og.jpg from the vector.
- [ ] Verify Space Grotesk **š đ č ć ž** at 500 and 700.
- [ ] `{VIBER_LINK}` — the only `{PLACEHOLDER}` still open in the copy.
- [ ] Telegram token and chat ID (parked by Marko; the endpoint gets built to read them from `/www/easy-config/config.php` regardless).
- [ ] **Spec inconsistency:** CLAUDE.md §3.8 says O nama is "2 short paragraphs," but the rewritten §5.7 has three. §5 copy is authoritative — building three. Flagging, not fixing.
