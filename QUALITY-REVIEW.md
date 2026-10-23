# Provera projekta — 11. septembar 2026.

Ispravljene su navigacija sa unutrašnjih stranica, obrada cena, dostupnost u katalogu,
Windows 10 tekst, nedostajuća OG slika i serverska obrada upita. Dodati su testovi,
provera tipova, deploy workflow i uputstvo za konfiguraciju. Astro je ažuriran na
7.3.2; poslednji npm audit pri instalaciji prijavio je 0 ranjivosti.

## Vizuelna i estetska provera

Ručno pregledani Chrome snimci početne strane, paketa, kontakta i kataloga na
360, 768 i 1440 px. Kompletne četiri stranice proverene su browser testovima na
istim širinama. Nema horizontalnog prelivanja cele stranice, nedostajućih slika,
JavaScript grešaka ni neuspelih mrežnih zahteva u lokalnom prikazu.

- Novi hero prikazuje konceptualnu IT opremu, sa mirnim osvetljenjem i bojama brenda.
- Naslov i glavni poziv na akciju ostaju najvažniji elementi početnog prikaza.
- Tipografija je lokalna: Space Grotesk 500/700 i IBM Plex Sans 400/600,
  latin + latin-ext; svih osam odgovarajućih font-face resursa učitano je u proveri.
- Paketi imaju jednake visine i poravnatu dugmad na desktopu; na telefonu se slažu vertikalno.
- Filteri kataloga na telefonu koriste vodoravno pomeranje; prikaz je ograničen na
  12 rezultata po stranici. Dinamički razmak drži kontakt formu ispod lepljive trake.
- Artikli ostaju bez izmišljenih fotografija konkretnih modela. Kategorija i brend
  u kartici daju jasniju hijerarhiju.
- Escape zatvara mobilni meni. Filteri imaju aria-pressed. Animacije i skrol
  poštuju prefers-reduced-motion.

## Rezultati

Lighthouse mobile, lokalni produkcioni build u Chrome-u, simulirano mobilno usporenje:

| Stranica | Performanse | Pristupačnost | Dobre prakse | SEO |
|---|---:|---:|---:|---:|
| Početna | 98 | 100 | 100 | 100 |
| Katalog | 98 | 100 | 100 | 100 |

Rezultati nisu merenje produkcionog VPS-a; mreža, keš i serverska podešavanja mogu
promeniti brojke. HTML/JSON izveštaji su u `artifacts/lighthouse/`.

- Astro build uspešan; četiri stranice i sitemap.
- Astro/TypeScript provera bez grešaka i upozorenja.
- 15 browser testova: prikazi, WCAG A/AA automatizovane provere, navigacija,
  paginacija/filteri, izbor artikla i čuvanje teksta nakon greške pri slanju.
- 5 Python testova: numerički i tekstualni Excel formati, odbijanje neispravnih
  iznosa, zaokruživanje i osvežavanje koje čuva ručne podatke.
- PHP syntax check i 22 tvrdnje o validaciji, anti-spam ograničenju i oba kanala.
- 6 lokalnih HTTP provera endpointa, uključujući bezbedan neuspeh bez konfiguracije
  i očuvanje/escaping teksta za korisnike bez JavaScripta.
- Ponovni uvoz postojećeg Excel-a nije promenio nijednu postojeću numeričku cenu.

## Šta zahteva server

Ovaj rad nije objavljen na VPS. Potrebno je uneti Telegram podatke u spoljašnju
konfiguraciju, podesiti dozvole za rate-limit direktorijum i GitHub deploy secrets.
Stvarni Telegram i email prijem nisu testirani; testovi koriste lokalne zamene
transporta i ne šalju poruke. PHP provera je izvršena na lokalnom PHP 8.5.10.

Viber i Cloudflare analitika ostaju isključeni dok se ne unesu odgovarajuće
opcione javne postavke. DNS i mail servis nisu menjani.

Snimci: `artifacts/visual/`. Vizuali: `public/images/it-system.webp`,
`public/images/it-system-640.webp`, `public/og.jpg`. Izvornici i tačni promptovi:
`artwork/`. Detalji rada i puštanja sajta: `README.md`.
