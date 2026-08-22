# EASY COMPUTERS — Revival Plan v1
*Prepared 18 Aug 2026 · Working doc for Marko · Execution partner: Claude Opus (Claude Code / chat)*

---

## 0. Ground rules (locked constraints)

- **Do not touch the 3 existing accounts.** They are life support. Only acceptable use: warm intros they volunteer or that dad requests casually ("znaš li nekog kome treba IT čovek?").
- **Budget ≈ 0.** Everything below runs on free tiers (Cloudflare Pages, GitHub, Telegram) + Marko's time.
- **Positioning:** One partner for SME IT — *oprema + licence + podrška* — not a webshop competing with Gigatron on price.
- **Website role:** Trust asset + lead capture. `/shop` is a curated showcase (upit → ponuda), **not** a full e-commerce catalog. No cart, no online payment in v1.
- **Domains:** `easy.rs` primary, `izi.rs` → 301 redirect.

---

## 1. Service catalog for Serbian SMEs (what to sell)

Target client: 5–30 employees, no internal IT, Belgrade + remote-friendly. Ranked by fit with Easy's existing strengths (hardware supply + trust).

| # | Usluga | Why it sells now |
|---|--------|------------------|
| 1 | **Paušalno IT održavanje** (mesečni ugovor: remote + on-site podrška, updates, AV nadzor) | Recurring revenue; the market standard offer; clients get predictable cost instead of a ~90–100k RSD/mes IT salary |
| 2 | **Nabavka i lifecycle opreme** (laptopovi, desktopovi, monitori, periferija, garancije, zamene) | Easy's core competence; attaches automatically to every retainer |
| 3 | **Windows 11 migracija + hardware refresh** | ⏰ Win10 security updates end **13 Oct 2026** (ESU Year 1 cutoff, ~8 weeks away). Business ESU costs $61/device/yr and doubles yearly — replacement often beats ESU. This is the #1 outreach hook right now. |
| 4 | **Microsoft 365 / licenciranje** (email na svom domenu, Office, Teams; Windows/Office licence) | Every SME needs it; sticky monthly; Easy already sells licenses |
| 5 | **Backup i zaštita podataka** (NAS + cloud backup, oporavak) | Fear-driven, high perceived value, sells hardware (NAS, diskovi) |
| 6 | **Mreže i Wi-Fi** (ruteri, svičevi, AP, kabliranje via podizvođač) | Project revenue + hardware attach; dad's contacts cover heavy installs |
| 7 | **Antivirus / endpoint zaštita** (ESET i sl., centralno upravljanje) | Cheap add-on, bundles into retainer |
| 8 | **Besplatan IT pregled** ("IT audit") | Not a revenue line — the **lead magnet / wedge**. 60–90 min on-site, produces a 1-page findings doc that surfaces hardware, license and support gaps. |

Deliberately **out of scope v1:** video nadzor, fiskalne kase, web development, custom software. (Subcontract or refer if asked.)

---

## 2. Placeholder pricing (validate in week 2 calls)

Market anchors found (Aug 2026): Belgrade IT firms start at **~2.000 RSD/h**; per-computer maintenance runs **4.000–6.000 RSD/računar/mes** (Data Inženjering); package models range up to **36.000+ RSD/mes sa PDV** for top tiers (TITI Računari); one budget player uses **2.500 fixed + 2.500/računar** (Čip IN); transport van BG ~24 RSD/km. Positioning: enter *slightly under* mid-market, win on responsiveness + hardware bundle.

**Sve cene usluga su bez PDV-a.** (Shop prices display sa PDV-om.)

### Ad-hoc (bez ugovora)
| Stavka | Cena |
|---|---|
| Remote intervencija | **2.500 RSD/h** (min 30 min) |
| Izlazak + rad na terenu (Beograd) | **3.500 RSD/h** (min 1h, izlazak uključen) |
| Teren van Beograda | + 30 RSD/km |
| Hitno / van radnog vremena | +50% |
| Prepaid blok 10h | **30.000 RSD** (−15%, važi 6 meseci) |

### Mesečni paketi (ugovor, otkaz uz 30 dana)
| | **START** | **STANDARD** | **BIZNIS** |
|---|---|---|---|
| Do broja računara | 5 | 10 | 20 + server/NAS |
| Cena / mes | **15.000 RSD** (~€130) | **28.000 RSD** (~€240) | **55.000 RSD** (~€470) |
| Remote podrška (pon–pet 9–17) | ✔ | ✔ | ✔ |
| Odziv | isti/sledeći radni dan | do 4h | do 2h |
| On-site poseta | po potrebi (naplata −20%) | 1× mesečno | 2× mesečno |
| Windows/driver updates, AV nadzor | ✔ | ✔ | ✔ |
| Backup nadzor | – | ✔ | ✔ + server/NAS |
| M365 administracija | – | ✔ | ✔ |
| Popust na opremu iz ponude | 3% | 5% | 7% |
| Alternativa po računaru | — | **2.500–3.000 RSD/računar/mes** (za nestandardne veličine) | |

### Projekti / jednokratno
| Stavka | Cena |
|---|---|
| Windows 11 migracija (backup podataka, instalacija, drajveri, prenos) | **4.000 RSD/računar**; 5+ mašina → 3.500 |
| Provera Win11 kompatibilnosti celog voznog parka | **besplatno uz pregled stanja** |
| M365 implementacija (domen, mailbox-i, migracija pošte) | **2.500 RSD po korisniku** jednokratno; licence po Microsoft CSP ceni (Basic ~$6–7.2, Standard ~$12.5–12.95, Premium ~$22–26.4 po korisniku/mes) |
| Backup setup (NAS + cloud, bez opreme) | od **15.000 RSD** |
| Mreža za kancelariju do 20 ljudi (bez opreme) | od **25.000 RSD** |
| IT pregled (audit) | **0 RSD** (navesti "vrednost 12.000 RSD") |

Margin logic: retainers price at ~⅓ of the cheapest alternative (part-time IT salary), hardware attach adds the real upside, and the audit is free because every audit historically converts into at least a quote.

---

## 3. Go-to-market (no cold-calling the 3 accounts)

1. **Win10 deadline campaign (primary wedge, run Sep–Oct):** "13. oktobra vaši Windows 10 računari ostaju bez bezbednosnih ispravki. Besplatno proveravamo koje mašine mogu na Windows 11 i šta se isplati zameniti." Every audit ends with a migration quote + hardware quote.
2. **List building:** 100–200 Belgrade SMEs (računovođe, advokati, špediteri, ordinacije, mali proizvođači, agencije) via Google Maps + APR + LinkedIn. Marko scrapes; dad flags anyone he knows for a warm touch.
3. **Channels:** email (small manual waves, 15–20/day), Viber/WhatsApp for warm ones, LinkedIn for agencies. GBP profile so "IT podrška Beograd" searches find something real.
4. **Referral ask (soft):** dad mentions the new services to friendly non-client contacts; never pitches the 3 accounts.
5. **Metric gate (day 30 after launch):** ≥ 10 audits booked or ≥ 3 quotes sent → continue; otherwise revise message/offer, not the website.

---

## 4. Website (summary — full spec in `CLAUDE.md`)

- **Stack:** Astro + Tailwind, static, deployed to the firm's **existing VPS** (aaPanel/nginx — the same box hosting mail.easy.rs, so DNS and dad's email stay untouched). GitHub Action auto-deploys on push. Forms via a tiny `upit.php` → Telegram (instant na telefon) **+ email na office@easy.rs** (lokalni mail server na istom VPS-u). No WordPress, no CMS, no new subscriptions.
- **Pages:** one-pager `/` (hero → trust bar → usluge → paketi/cene → Win10 banner → proces → o nama → FAQ → kontakt) + `/shop` (curated 30–60 SKUs, "Pošalji upit" per product) + `/hvala`.
- **Language:** sr-Latn only in v1.
- **SEO targets:** "IT podrška za firme Beograd", "održavanje računara za firme", "prodaja računarske opreme za firme", "prelazak na Windows 11".
- **`/shop` rules:** cene sa PDV; volatile items = "cena na upit"; disclaimer "cene potvrđujemo uz ponudu"; availability = "kod dobavljača, isporuka 1–3 radna dana"; za pravna lica predračun.
- **Seeding without feeds:** the old aggregator stays dead. v1 is manual curation — 30–60 SKUs copied from dad's B2B portal exports, converted via Prompt P3, human-checked line by line (~2–3h). Every item carries a `supplier_sku` from the chosen refresh supplier.
- **v1.1 — price & availability refresher (post-launch, time-boxed 2–3 days):** one supplier's weekly XLS export → script matches by šifra against the curated products.json → updates price + availability *only* for existing items, flags SKUs missing from the feed (verovatno EOL) → commit triggers Pages redeploy. One supplier + one key = no matching problem; curation stays human, freshness goes automatic. This normalizer is also module #1 of any future B2B quoting engine.

---

## 5. Brand kit — AI tools & how to use them

**Decision:** the name stays **"Easy Computers"** — 27 years of equity; the lockup does the shortening ("easy" dominant, "computers" small). A logo already exists on the ponuda template (navy `#17334A` / blue `#2F9FDB`), so Day 1 starts with **reuse-vs-refresh**, not from zero. Signature motif: a small **green status dot** (● "sve radi") — honest to the subject (uptime), reusable everywhere (bullets, favicon, hover states). Palette: ink `#12161C`, paper `#FAFAF7`, steel `#5B6470`, signal green `#17A34A`, one restrained accent (cobalt `#2450E6`) — avoid the generic cream+terracotta and black+acid-green AI defaults. Type: **Space Grotesk** (display) + **IBM Plex Sans** (body — excellent š/đ/č/ć/ž coverage).

| Job | Tool | Notes |
|---|---|---|
| Logo concepts | **Ideogram** (ideogram.ai) | Best free option for text-in-logo; generate 20+, shortlist 3 |
| Vector/SVG logo | **Recraft** (recraft.ai) | Exports real SVG — critical for web/print |
| Auto-vectorize a raster pick | vectorizer.ai or Inkscape trace | Backup path |
| Full identity in a box | Looka / Brandmark | Paid one-time; only if Ideogram results disappoint |
| Palette | **Coolors** + **Huemint** | Lock ink/paper first, generate accents |
| Palette on a real UI | **Realtime Colors** (realtimecolors.com) | Sanity-check before coding |
| Type pairing | Fontjoy + typescale.com | Stay on Google Fonts (free, fast) |
| Contrast check | whocanuse.com | AA minimum on all text |
| Favicon set | realfavicongenerator.net | From the SVG mark |
| OG/social images | Figma (free) or Canva | 1200×630 template with dot motif |

**Ready logo prompts (paste into Ideogram/Recraft):**
> minimalist wordmark logo, lowercase "easy", geometric sans-serif, a small green circle dot integrated after the word, tech company, flat vector, white background, no gradients, no 3D
>
> logo for IT support company "easy", abstract mark combining a power symbol and a checkmark, single color deep navy, flat minimal vector, lots of whitespace

---

## 6. Step-by-step execution plan

**Day 0 — Decisions & assets (Marko, 2–3h)**
- [ ] Confirm open questions (section 8) with dad
- [ ] Collect remaining legal data: PIB, MB, adresa (naziv ✅ Easy Computers J2M d.o.o. · kontakt ✅ +381 63 1111727 / office@easy.rs · osnovana ✅ 1999.)
- [ ] In aaPanel Mail Server: create **office@easy.rs** mailbox if it doesn't exist (+ **web@easy.rs** as the form's sender)
- [ ] Create Telegram bot (@BotFather) → token + chat ID for the upit form

**Day 1 — Brand sprint (Marko + tools, 1–3h)**
- [ ] Decide: keep the existing ponuda logo (fast path — vectorize it if it's raster) or refresh
- [ ] If refreshing: run logo prompts, shortlist 3, pick 1, get SVG
- [ ] Lock palette + fonts (use suggested direction as default)
- [ ] Generate favicon set + OG image

**Day 1–3 — Website build (Opus in Claude Code)**
- [ ] New GitHub repo `easy-site`, drop `CLAUDE.md` in root
- [ ] Kick off with **Prompt P2**; review each section as it lands
- [ ] Deploy preview on Cloudflare Pages

**Day 2–3 — Shop data (Marko + Opus)**
- [ ] Pick 30–60 SKUs from supplier lists across 8 categories (things you actually move: SSDs, RAM, monitori, laptopovi, periferija, mrežna oprema, štampači, licence)
- [ ] Use **Prompt P3** to convert supplier rows → `products.json`
- [ ] Manually sanity-check every price and name (no automated matching = no duplicate mess)

**Day 3–4 — Launch (VPS)**
- [ ] GitHub Action → rsync `dist/` into the easy.rs webroot (site entry stays PHP 8.1 for upit.php); DNS/mail untouched
- [ ] Create `/www/easy-config/config.php` on the server (TG token + chat ID + mail to/from, outside webroot)
- [ ] Verify izi.rs **and** www.easy.rs both 301 → https://easy.rs
- [ ] Test form → Telegram **i** email u office@easy.rs; Lighthouse ≥ 90 mobile; Cloudflare Web Analytics snippet on
- [ ] Server housekeeping: weekly aaPanel backups ON for easy.rs **i mail**; archive/disable usluge.easy.rs (backup 820 dana star, ~480k bot zahteva); strong panel password + non-default port
- [ ] Google Business Profile (Prompt P5 for texts), LinkedIn company page, new email signatures

**Week 2 — Validate & load the pipeline**
- [ ] 5 validation calls with friendly business owners from dad's wider circle (NOT the 3 clients): read them the paketi page, ask "šta bi vas nateralo da potpišete / šta fali / da li je cena čudna" — adjust prices once
- [ ] Build outreach list (100+ firms) — Prompt P4 generates the templates + audit checklist
- [ ] Send wave 1 (Win10 hook), 15–20/day, track in a sheet

**Week 3+ — v1.1: price & availability refresher (only after wave 1 is out)**
- [ ] ✅ Supplier = **EWE** (portal XLSX verified: `Ident`, `Naziv`, `Cena sa popustom`, `Lager`, `Opis`; ~5.7k unique products). Remaining: dad confirms "Cena sa popustom" je **bez PDV-a** + that publicly listing derived prices is OK
- [ ] Build with **Prompt P6**; hard time-box 2–3 days, then stop regardless
- [ ] Weekly loop: download XLS (2 min) → run script → review diff → commit (Pages auto-redeploys)

**Day 30 — Gate**
- [ ] ≥ 10 audits booked or ≥ 3 quotes out → double down. Below that → fix the message/offer with Opus, resend; the site itself is done.

---

## 7. Opus prompt library (copy-paste)

**P6 — /shop price refresher** *(Claude Code, post-launch, v1.1)*
```
Build scripts/refresh-prices.py. Input: the EWE portal XLSX dropped into
/pricefeeds/ (sheet "ewe"; columns: Ident = supplier_sku, Naziv, PMP = preporučena
maloprodajna cena SA PDV-om, "Cena sa popustom" = our internal buy price, Lager =
integer stock). Prices come as "36.960,00 RSD" — strip suffix, dot = thousands,
comma = decimal. The same Ident appears on multiple rows (one per category) —
group by Ident, keep first, but take PMP from any row that carries it.
For every product in src/data/products.json that has a supplier_sku and
auto_price=true:
  new price_rsd = PMP × 1.05, rounded to nearest …90 under 10.000 and nearest
  …990 at 10.000+. NO VAT MATH — never multiply by 1.20, there is no margin map.
  If PMP is empty for that Ident in this export: leave price_rsd untouched and
  list it under "PMP nestao — proveri", never fall back to "Cena sa popustom".
  If the computed price lands below "Cena sa popustom": skip the write and flag
  it as "ispod nabavne — proveri".
  availability: lager > 0 → "Na stanju kod dobavljača — isporuka 1–3 radna dana",
  else → "Trenutno nedostupno" and featured=false.
Then print a diff table: old→new price per item, availability changes, and SKUs
present in products.json but missing from the feed (flag as "verovatno EOL — proveri").
Hard rules: "Cena sa popustom" is internal — it must never be written into
products.json or printed anywhere public; read the šifra column as text (dtype=str —
leading zeros must survive); never add new products, never modify
name/short_desc/specs, never touch auto_price=false items, and exit nonzero without
writing if >30% of prices changed (that's a broken file, not a market move).
Write changes only after I confirm.
```

**P1 — Brand brief refinement** *(chat, optional)*
```
Context: reviving "Easy Computers" (easy.rs), a Belgrade family business selling IT
equipment, now adding SME IT support services. Audience: owners of 5–30 person
Serbian firms, non-technical, value reliability over flash.
Task: critique this brand direction [paste section 5 direction + my shortlisted
logos as images]. Score each logo on: distinctiveness, scalability at 16px,
Serbian B2B credibility. Recommend one and give exact hex/font tokens for the site.
```

**P2 — Website build kickoff** *(Claude Code, repo root contains CLAUDE.md)*
```
Read CLAUDE.md fully before writing any code. Build the site exactly per that spec.
Work in this order: (1) scaffold + design tokens, (2) index page section by section
with the provided Serbian copy, (3) /shop from products.json, (4) upit form + PHP
endpoint + deploy workflow, (5) SEO/meta/sitemap, (6) Lighthouse pass. After each stage, stop and
show me the result before continuing. If the spec is ambiguous, ask — do not invent
new sections, do not change the copy's meaning, do not add a cart.
```

**P3 — Supplier list → products.json** *(chat or Claude Code)*
```
I'm pasting rows from a supplier price list (format varies: Excel paste / PDF text).
Convert ONLY the rows I marked into JSON matching this schema: [paste schema from
CLAUDE.md §6]. Rules: supplier_sku = the Ident column (as text); slug = kebab-case name; price_rsd = my selling price which is
supplier price × (1 + margin I give per category) rounded to nearest 90/990;
if I write "upit" for price, set price_rsd null and price_note "Cena na upit".
Treat šifra (supplier_sku) as text — leading zeros must survive.
Do not merge or dedupe rows — I curate manually. Output valid JSON only.
```

**P4 — Outreach kit** *(chat)*
```
Context: [paste plan sections 1–3]. Generate in Serbian (sr-Latn), poslovni ali
ljudski ton, no corporate filler:
1) Cold email, Win10 hook, <120 words, subject + 2 varijante prvog pasusa
2) Viber/WhatsApp poruka, <60 words, za polu-tople kontakte
3) LinkedIn poruka za vlasnike agencija, <80 words
4) Follow-up email posle 5 dana, <60 words
5) "IT pregled" checklist — 1 strana, 12–15 stavki koje proveravamo
   (računari/Win11 spremnost, backup, licence, mreža, mail, bezbednost), sa poljem
   za nalaz i preporuku — formatiran kao markdown koji mogu da odštampam.
```

**P5 — GBP + SEO texts** *(chat)*
```
Write in Serbian: (1) Google Business Profile description, 720 chars, category
"IT support and services", Beograd, mentioning oprema + održavanje + Windows 11;
(2) meta title + description for / and /shop within Google pixel limits;
(3) 5 GBP posts I can schedule (Win10 rok, besplatan pregled, paketi, oprema, backup).
No superlatives without substance, no keyword stuffing.
```

---

## 8. Open questions — status (updated 18 Aug)

1. ✅ Legal: **Easy Computers J2M d.o.o.** (site displays "Easy Computers"). Still needed for footer: PIB, MB, adresa.
2. ✅ Founded **1999** → trust bar "Od 1999. godine"; sold-units counter dropped (unknown number = don't claim it).
3. ✅ Name: **Easy Computers** stays; lockup emphasizes "easy".
4. ✅ Contact: **+381 63 1111727 · office@easy.rs**. Confirm: ko se javlja na upite radnim danom?
5. ✅ Photos: none at launch — typographic v1; shoot 5 phone photos (radnja, magacin, radni sto) for v1.1.
6. ✅ Supplier prices: **EWE B2B portal XLSX export** (verified sample: 6.720 rows / 5.726 unique Ident-a — duplicates are category re-listings, solved by group-by). Remaining check with dad: "Cena sa popustom" je bez PDV-a? + terms allow publicly listing derived prices.
