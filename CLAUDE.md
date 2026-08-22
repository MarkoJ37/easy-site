# CLAUDE.md — easy.rs website build brief

You are building the public website for **Easy Computers** (`easy.rs`) — a Belgrade family business (25+ years) selling IT equipment to companies, now expanding into SME IT support services. The site's job: make a small-business owner trust us enough to (a) request a **besplatan IT pregled** or (b) send a product **upit**. It is a lead-capture and credibility site, **not** an e-commerce store.

## 0. Hard rules

- Language: **Serbian, latinica (sr-Lat)**. All UI copy, meta, and errors in Serbian. Copy provided in §5 — use it verbatim unless it breaks layout; never change its meaning.
- **No** cart, checkout, payments, user accounts, CMS, cookie banners, or third-party trackers. Analytics = Cloudflare Web Analytics beacon only.
- **No** stock photos of "smiling support agents with headsets". Use provided real photos; where a visual is needed and no photo exists, use typographic/graphic treatment instead.
- Every price in `/shop` renders with "sa PDV-om" context and the global disclaimer (§6). Service prices on `/` are "bez PDV-a" and marked as such.
- Do not invent services, claims, or numbers not present in this brief. `{PLACEHOLDER}` tokens must remain grep-able until Marko replaces them.
- Ask before deviating from this spec. Do not add sections.
- **Terminology (changed 18 Aug 2026):** the lead magnet is a **"IT pregled"**, never "snimak". Marko rejected "snimak IT stanja" as a literal translation from English. Derived forms in use: nav CTA `Besplatan IT pregled` · hero/paketi CTA `Zakažite besplatan pregled` / `Zakažite pregled` · Proces step 1 `Pregled stanja` · FAQ `Koliko košta IT pregled?` · kontakt heading `Zakažite besplatan pregled IT sistema`. Note `Zakažite proveru` stays the Win10 banner's CTA — it is a different, narrower offer (Win11 compatibility only).

## 1. Stack & repo

- **Astro 7** (static output) + **Tailwind CSS v4** + `@astrojs/sitemap`. (Brief originally pinned Astro 5; Marko approved the upgrade to 7.2.3 on 18 Aug 2026 — build verified clean, no code changes were needed.) No React needed; use Astro components + a little vanilla JS (shop filter, mobile nav, form submit).
- Hosting: **the firm's existing VPS** (aaPanel + nginx — the box already serving easy.rs and mail.easy.rs). The easy.rs site entry stays a **PHP 8.1 project** so the static build and one PHP endpoint coexist. **DNS does not change**: all @easy.rs mail lives on this server — MX/SPF records are out of this project's scope, never touch them.
- Deploy: GitHub Action on push to main → `npm run build` → rsync `dist/` over SSH into the easy.rs webroot. Secrets: `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_KEY`, `DEPLOY_PATH`. Form endpoint: `public/api/upit.php`.
- Node 20+. Package manager: npm.

```
easy-site/
├─ CLAUDE.md
├─ astro.config.mjs            # site: https://easy.rs, sitemap integration
├─ src/
│  ├─ styles/global.css        # tokens as CSS vars + Tailwind
│  ├─ data/
│  │  ├─ products.json
│  │  └─ site.ts               # single source: brand "Easy Computers" · legal "Easy Computers J2M d.o.o."
│  │                           # tel +381 63 1111727 · email office@easy.rs · PIB 102699654 · MB 17458795
│  │                           # adresa: Veljka Petrovića 67, 11030 Beograd
│  ├─ components/              # Nav, Hero, TrustBar, Services, Paketi, Win10Banner,
│  │                           # Proces, ONama, Faq, Kontakt, Footer, ProductCard,
│  │                           # ShopFilter, UpitForm
│  ├─ layouts/Base.astro       # meta, OG, JSON-LD, fonts
│  └─ pages/
│     ├─ index.astro
│     ├─ shop/index.astro
│     ├─ hvala.astro
│     └─ privatnost.astro      # short, plain-language
├─ .github/workflows/deploy.yml  # build + rsync dist/ → VPS webroot on push
└─ public/  (logo.svg, favicon set, og.jpg, robots.txt, photos/, api/upit.php)
```

## 2. Design system

Two-pass process: **first** write a short design plan (palette, type scale, layout wireframe in comments, the signature element) into `DESIGN-NOTES.md`; self-critique it — if any part looks like a generic template you'd produce for any IT company (or like the usual AI defaults: cream+terracotta serif look, or near-black + acid-green), revise it — **then** code, deriving every visual decision from the approved tokens.

Starting tokens (Marko may override after brand sprint — read from `global.css` vars):

```css
--ink:    #12161C;  /* text, headings */
--paper:  #FAFAF7;  /* background */
--steel:  #5B6470;  /* secondary text, borders */
--signal: #17A34A;  /* the status-dot green — accents, success, CTA hover */
--accent: #2450E6;  /* links, primary CTA */
```

- **Existing brand:** a logo + palette already live on the firm's ponuda template (navy `#17334A`, blue `#2F9FDB`). If Marko keeps that logo, shift `--ink`/`--accent` toward those values so website and PDF ponude match. The green status dot stays either way.
- **Wordmark:** "Easy Computers" — "easy" set dominant, "computers" small/secondary in the lockup. The 27-year name stays; typography does the shortening (easy.rs reinforces it).
- Type: **Space Grotesk** (display, weights 500/700, used sparingly) + **IBM Plex Sans** (body, 400/600). Both from Google Fonts, subset latin-ext (š đ č ć ž must render correctly — verify).
- **Signature element:** the small green **status dot** ("● sve radi"). Use it as: pulse-dot next to the hero eyebrow, list markers in paketi, availability indicator in shop, favicon core. This is the one memorable device — keep everything else quiet and disciplined.
- Layout: generous whitespace, max-w ~1100px, clear section rhythm. Light theme. Border radius small (6–8px). One restrained scroll-reveal on section entry is enough; respect `prefers-reduced-motion`.
- Quality floor: responsive to 360px, visible keyboard focus states, semantic landmarks, AA contrast everywhere.

## 3. Pages & sections (index, in order)

1. **Nav:** logo · Usluge · Cene · Oprema (→ /shop) · Kontakt · CTA button "Besplatan IT pregled". Sticky, slim.
2. **Hero:** eyebrow with pulse dot "● IT partner za mala preduzeća" (Marko dropped the "— Beograd" suffix 18 Aug; the city still carries in the hero sub, TrustBar and JSON-LD); H1 + sub from §5; primary CTA "Zakažite besplatan pregled" (scroll to #kontakt), secondary "Pogledajte opremu" (/shop).
3. **TrustBar:** 4 short facts: "Od 1999. godine" · "Oprema i podrška na jednom mestu" · "Odziv istog radnog dana" · "Beograd + remote, cela Srbija". (No unverifiable counters — 27 years is the number that matters.)
4. **Usluge:** 6 cards (copy §5.3). Each: icon (simple line style, consistent set — lucide), title, 2 lines, no "learn more" links.
5. **Paketi (#cene):** 3 pricing cards START/STANDARD/BIZNIS from §5.4 + ad-hoc line below + note "Sve cene su bez PDV-a. Ugovor se raskida uz otkazni rok od 30 dana — bez vezivanja." STANDARD visually featured.
6. **Win10Banner:** full-width, urgent-but-calm strip (copy §5.5) with CTA to #kontakt. Countdown text is static copy, not a JS countdown.
7. **Proces:** 3 numbered steps (real sequence, numbering justified) from §5.6.
8. **O nama:** 2 short paragraphs (§5.7). Photos are v1.1 — until real ones exist, use a typographic/graphic treatment (never stock).
9. **FAQ:** accordion, 6 items (§5.8), native `<details>`.
10. **Kontakt (#kontakt):** UpitForm (§4) + direct contacts from `site.ts` (tel link, mailto, Viber/WhatsApp link `{VIBER_LINK}`), radno vreme.
11. **Footer:** legal (Easy Computers J2M d.o.o., PIB 102699654, MB 17458795, Veljka Petrovića 67, 11030 Beograd), linkovi (Privatnost), © year, quiet dot.

`/shop`: header + disclaimer strip (§6), category filter chips + client-side search, responsive grid of ProductCards, each card → "Pošalji upit" opens prefilled UpitForm (modal or scroll with product name injected). `/hvala`: short confirmation + "Javljamo se u roku od jednog radnog dana." + back link.

## 4. Upit form + PHP endpoint

Fields: Ime i prezime* · Firma · Telefon* · Email · Broj računara (select: 1–5 / 6–10 / 11–20 / 20+ / nije bitno) · Poruka* · hidden `proizvod` (prefill from shop) · honeypot `website` (hidden) · `ts` (render timestamp).

`public/api/upit.php` (Astro copies `public/` verbatim, so it lands in `dist/api/` and nginx+PHP serves it): POST form/JSON → validate (required fields, honeypot empty, `time() - ts > 3`) → deliver through **two channels**:

1. **Telegram** — Bot API sendMessage, all fields one per line, prefixed "🟢 UPIT sa easy.rs".
2. **Email** — to `office@easy.rs` via the VPS's own mail server (try PHP `mail()` first; if it doesn't deliver, switch to SMTP localhost with a `web@easy.rs` mailbox). From: `web@easy.rs`, Reply-To: visitor's email when given, subject `Upit sa easy.rs — {ime} ({firma})`, plain-text body with all fields. Same-box local delivery → no SPF/deliverability issues.

Respond 200 and redirect to `/hvala` if **at least one** channel succeeded; `error_log` whichever failed. Config via `require '/www/easy-config/config.php'` — constants `TG_TOKEN`, `TG_CHAT`, `MAIL_TO`, `MAIL_FROM` (+ SMTP creds only if the `mail()` route fails), **outside every webroot**, created once on the server, never committed to git. If both channels fail: inline Serbian error "Nešto nije prošlo. Pozovite nas ili pišite na office@easy.rs." Never lose the user's text.

## 5. Copy (Serbian — use as written)

**5.1 H1:** `Računari, mreža i licence — da jednostavno rade.`
**Sub:** `IT oprema i podrška za mala preduzeća. Jedan partner, predvidiv mesečni trošak, bez komplikacija — u Beogradu i remote, širom Srbije.`

**5.3 Usluge (title — description):**
- `Održavanje i podrška` — `Remote i na terenu. Mi brinemo o računarima, vi o poslu.`
- `Nabavka opreme` — `Laptopovi, računari, monitori i periferija — po veleprodajnim uslovima, sa garancijom i našom podrškom.`
- `Prelazak na Windows 11` — `Proveravamo koje mašine mogu na Windows 11, selimo podatke i menjamo ono što se ne isplati krpiti.`
- `Microsoft 365 i licence` — `Email na vašem domenu, Office i Teams — legalno, podešeno i održavano.`
- `Backup i zaštita podataka` — `Automatski backup na NAS i u cloud. Da jedan pokvaren disk ne postane katastrofa.`
- `Mreže i Wi-Fi` — `Stabilna mreža u kancelariji, magacinu i lokalu — projektovanje, oprema i održavanje.`

**5.4 Paketi:** names START / STANDARD / BIZNIS; prices 15.000 / 28.000 / 55.000 RSD mesečno; bullets per plan doc §2 (do 5/10/20+server računara; odziv sledeći radni dan / do 4h / do 2h; on-site po potrebi / 1× / 2× mesečno; svi: remote podrška, updates i AV nadzor; STANDARD+: backup nadzor i M365 administracija; popust na opremu 3/5/7%). Ad-hoc line: `Bez ugovora: remote 2.500 RSD/h · teren u Beogradu 3.500 RSD/h · prepaid 10h = 30.000 RSD.`

**5.5 Win10Banner:** `Windows 10 od 13. oktobra 2026. ostaje bez bezbednosnih ispravki.` + `Besplatno proveravamo koje vaše mašine mogu na Windows 11 — i šta je jeftinije zameniti nego produžavati. Bez obaveze.` CTA: `Zakažite proveru`.

**5.6 Proces:** 1 `Pregled stanja` — `Dolazimo (ili se povezujemo remote), prolazimo kroz opremu, licence, backup i mrežu. Traje do sat vremena.` 2 `Predlog i cena` — `U roku od 48h dobijate jednu stranu: šta je dobro, šta je rizik i šta predlažemo — sa cenom.` 3 `Preuzimamo brigu` — `Potpisujemo ugovor bez vezivanja i od prvog dana imate koga da pozovete.`

**5.7 O nama:** `## O nama`

`Easy Computers je porodična firma iz Beograda. Počela je 1999. godine, iz`
`opsesije računarima u vreme kada je malo ko u Srbiji znao šta će s njima —`
`i od tada radi isti posao: nabavlja opremu firmama i stara se da ta oprema`
`radi.`

`Danas je vodimo otac i sin. Ta kombinacija je i razlog zašto nam se`
`klijenti vraćaju: iza svake ponude stoji 27 godina iskustva sa dobavljačima`
`i garancijama, a iza podrške neko ko poznaje i savremene sisteme, mreže i`
`cloud servise.`

`Radimo sa firmama koje nemaju svoje IT odeljenje i kojima treba jedan broj`
`telefona umesto pet dobavljača. Ne prodajemo ono što ne bismo sami`
`koristili, ne naplaćujemo ono što nismo uradili i javljamo se kada`
`zovete — i posle isporuke.`

**5.8 FAQ (Q — A):**
- `Da li moramo da kupujemo opremu kod vas?` — `Ne. Održavamo i opremu kupljenu bilo gde. Naši klijenti obično vremenom pređu na nabavku kod nas — jer je jednostavnije i jer imaju popust.`
- `Da li postoji vezivanje ugovorom?` — `Ne. Mesečni paketi se raskidaju uz otkazni rok od 30 dana.`
- `Šta ako imamo "svog čoveka" za IT?` — `Odlično — možemo da pokrivamo ono što on ne stiže: hitne intervencije, nabavku, licence ili samo backup.`
- `Koliko brzo reagujete?` — `Remote najčešće u roku od sat-dva. Na teren u Beogradu izlazimo isti ili sledeći radni dan, po paketu i do 2h.`
- `Radite li van Beograda?` — `Da — remote pokrivamo celu Srbiju, a teren van Beograda uz putne troškove.`
- `Koliko košta IT pregled?` — `Ništa. To je sat vremena našeg rada i jedna strana nalaza — vredi 12.000 RSD, ali je besplatan jer je najbolji način da se upoznamo.`

**5.9 Meta:** title `Easy Computers — IT oprema i podrška za firme | Beograd`; description `Održavanje računara, nabavka opreme, Microsoft 365 i prelazak na Windows 11 za mala preduzeća. Besplatan IT pregled. Beograd i cela Srbija.`

## 6. /shop data & rules

`src/data/products.json` — array of:

```json
{
  "id": "ssd-samsung-990-pro-1tb",
  "slug": "ssd-samsung-990-pro-1tb",
  "name": "Samsung 990 PRO 1TB NVMe SSD",
  "category": "Komponente",            // Laptopovi | Monitori | Komponente | Periferija |
                                        // Softver i licence
                                        // (Računari / Mrežna oprema / Štampači have zero
                                        //  PMP-populated items in the EWE feed — categories
                                        //  dropped, not padded. Re-add if a later export
                                        //  carries PMP for them.)
  "brand": "Samsung",
  "short_desc": "PCIe 4.0, do 7.450 MB/s — za ozbiljno ubrzanje radnih mašina.",
  "specs": ["1TB", "PCIe 4.0 x4", "5 god. garancije"],
  "price_rsd": 18990,                   // null → show price_note
  "price_note": null,                   // e.g. "Cena na upit"
  "image": "/photos/products/{file}.webp",  // if missing → typographic placeholder card
  "availability": "Kod dobavljača — isporuka 1–3 radna dana",
  "featured": false,
  "supplier_sku": "KT-990PRO1TB",       // supplier's šifra — key for the v1.1 price refresher; null = manual item
  "auto_price": true                    // false → refresher never touches this item's price
}
```

**Pricing rule (settled — no VAT math anywhere):** `price_rsd = PMP × 1.05`, rounded to the nearest `…90` under 10.000 RSD and the nearest `…990` at 10.000+. `PMP` is EWE's preporučena maloprodajna cena and is treated as **sa PDV-om**; never multiply by 1.20. The `Cena sa popustom` column is the internal buy price and **must never appear on the site or in `products.json`**. Only items with a populated PMP are eligible — no per-category margin map, no fallback to `Cena sa popustom`. Guard: skip any item where the computed price lands below the buy price (2 items in the current export do).

`Softver i licence` is populated by hand (M365, Windows, Office) with `price_rsd: null`, `price_note: "Cena na upit"`, `supplier_sku: null`, `auto_price: false` — it never comes from the EWE pass.

Rules: prices display `18.990 RSD` + small `sa PDV-om`; global strip on /shop: `Cene se menjaju sa kursom i lagerom dobavljača — svaku potvrđujemo uz ponudu. Za pravna lica: predračun i plaćanje po dogovoru.` Sort: featured first, then category, then name. Filter + search are client-side, no page reloads. Seed `products.json` from the ticked items in `SHOP-CANDIDATES.md` (target 30–60). No product photos at launch — every card renders the typographic treatment; the `image` field stays in the schema so photos can drop in later without a migration. A separate refresher script (v1.1, built post-launch) will update `price_rsd`/`availability` by `supplier_sku` and commit — the site must build and render correctly with or without it.

## 7. SEO / structured data

- JSON-LD `LocalBusiness` (name, url, telephone, address: streetAddress "Veljka Petrovića 67" / postalCode "11030" / addressLocality "Beograd" / addressCountry "RS", areaServed Beograd/Srbija, openingHours) in Base layout; `ItemList` on /shop is unnecessary — skip.
- Canonicals, OG (og.jpg 1200×630), `robots.txt` allow all, sitemap auto. `lang="sr-Latn"`.
- Redirects (nginx on the VPS, not in code): the `izi.rs` redirect site already exists in aaPanel — verify it 301s to `https://easy.rs`; set `www.easy.rs` → 301 apex the same way. DNS records stay exactly as they are.

## 8. Definition of done

- [ ] `npm run build` clean; GitHub Action deploy green; https://easy.rs serves the new site
- [ ] Lighthouse mobile: Performance ≥ 90, A11y ≥ 95, SEO ≥ 95
- [ ] Form verified end-to-end: Telegram ping arrives **and** email lands in office@easy.rs (inbox, not spam); honeypot + time-trap tested
- [ ] Mail server untouched: office@easy.rs sends & receives normally after deploy
- [ ] All `{PLACEHOLDER}` tokens either replaced or listed for Marko in final report
- [ ] š/đ/č/ć/ž render correctly in both fonts, all weights
- [ ] 360px, 768px, 1440px screenshots reviewed
- [ ] No console errors; no external requests except fonts + CF beacon

## 9. Working style

Build in the stage order given in the kickoff prompt; stop after each stage for review. Prefer deleting to adding. When copy and layout conflict, shorten the layout, not the meaning. If something in this brief is ambiguous or seems wrong — ask Marko, don't improvise.
