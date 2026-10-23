# Easy Computers

Statički poslovni sajt za IT opremu i podršku malim preduzećima. Astro + Tailwind,
četiri stranice i PHP endpoint za kontakt. Katalog ima 149 artikala dobavljača i
tri ručno održavane stavke za Microsoft licence. Nema korpe ni naplate.

## Lokalni rad

Node >=22.12.0, npm, Python 3.12 za osvežavanje cena. PHP >=8.1 sa cURL ekstenzijom
za endpoint; za produkciju koristiti podržano PHP izdanje.

```sh
npm ci
python -m pip install -r requirements-dev.txt
npm run dev
npm run check
npm run test:prices
php -l public/api/upit.php
php tests/upit_test.php
npm run build
npx playwright install chromium
npm test
```

Na Windowsu testovi koriste instalirani Google Chrome; na Linuxu Playwright Chromium.
PowerShell sa zabranjenim `.ps1` skriptama: koristiti `npm.cmd` umesto `npm`.
Astro preview služi statički sajt; PHP se proverava zasebno. Browser testovi presreću
slanje forme lokalno i ne šalju stvarne poruke.

## Katalog

`src/data/products.json` je izbor za objavljivanje. Dodavanje i uklanjanje proizvoda
radi se tu; osvežavanje ne uvozi ceo feed i čuva ručne stavke i uređene opise:

```sh
python scripts/seed-products.py --input ewe/novi-export.xlsx
```

Cena = PMP × 1.05, uz postojeće zaokruživanje. Nema dodatnog obračuna PDV-a.
Nepostojeći PMP ili cena ispod nabavne daje „Cena na upit“ za postojeći artikal.
Dostupnost i rok se potvrđuju uz ponudu; statički katalog ne tvrdi da prikazuje živ lager.
Excel i nabavne cene se ne objavljuju. `SHOP-CANDIDATES.md` je interni istorijski izbor.

## Produkciona konfiguracija

1. Kopirati `deploy/config.example.php` u `/www/easy-config/config.php` na VPS-u.
   Uneti TG_TOKEN i TG_CHAT lokalno na serveru. MAIL_TO i MAIL_FROM su definisani u primeru.
2. Kreirati `/www/easy-config/rate-limit`, dati PHP korisniku prava pisanja samo u taj
   poddirektorijum. Konfiguracija treba da bude čitljiva PHP korisniku, bez javnog pristupa.
   Stare rate-limit fajlove može uklanjati dnevni cron nakon jednog dana.
3. Sačuvati postojeću aaPanel PHP/nginx konfiguraciju i mail servis. PHP fajl mora da se
   izvršava preko PHP-FPM-a, a ne da se isporučuje kao tekst. Isključiti display_errors.
4. GitHub secrets: DEPLOY_HOST, DEPLOY_USER, DEPLOY_KEY, DEPLOY_PATH i DEPLOY_KNOWN_HOSTS.
   DEPLOY_PATH mora biti konkretan direktorijum sajta unutar `/www/wwwroot/`.
   SSH host key proveriti nezavisno preko administratorskog pristupa pre upisa u secret.
5. GitHub environment `production`; po želji podesiti pregled pre deploya.
   Workflow proverava tipove, cene, PHP, build i browser testove pre rsync-a.
   Upload ne briše stare fajlove: postojeći `.well-known` i drugi serverski fajlovi ostaju.
   Stari sajt arhivirati zasebno pri prvom puštanju, nakon provere sadržaja webroot-a.
6. Opcione GitHub variables / lokalni `.env`: PUBLIC_CF_BEACON_TOKEN (32 hex znaka)
   i PUBLIC_VIBER_LINK. Prazne vrednosti ne prikazuju neaktivne servise; privatnost prati stanje analitike.

Forma pokušava Telegram i PHP mail nezavisno; uspeh jednog kanala dovoljan je za
potvrdu. PHP mail prihvatanje nije dokaz da je poruka stigla u inbox. Pre puštanja
proveriti stvarni prijem na oba kanala, neuspeh oba kanala i anti-spam ponašanje.
Ako lokalni mail ne isporučuje poruke, potrebno je podesiti SMTP prema konkretnom serveru.
DNS, MX/SPF i mail servis nisu deo ovog deploya.

## Vizuali i provere

Nova konceptualna ilustracija je `public/images/it-system.webp` (uz manju 640px verziju).
Slika za deljenje je `public/og.jpg`, 1200 × 630. Izvornici i promptovi su u `artwork/`.
Ne predstavljaju fotografije firme ili konkretne artikle iz kataloga.
Snimci browser provere čuvaju se u `artifacts/visual/`.
