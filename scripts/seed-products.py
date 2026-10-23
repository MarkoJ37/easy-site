# -*- coding: utf-8 -*-
"""
Refresh the selected src/data/products.json catalog from the EWE portal XLSX.

Preserves manual products and editorial fields; never imports unselected items.
Rules are Marko's, settled 18 Aug 2026:
  * only items with a populated PMP are eligible
  * price_rsd = PMP x 1.05, rounded to nearest ...90 under 10.000 / ...990 above
  * PMP is treated as SA PDV-om — no VAT math anywhere
  * "Cena sa popustom" is the internal buy price and never leaves this script
  * skip anything whose computed price lands below the buy price

short_desc is written from the product NAME, not from the Opis column. Opis is a
raw spec dump whose values run together, and the EWE names are already precise
Serbian ("KM5221W Pro Wireless YU tastatura + miš crna"), so the name is both
more reliable and closer to how a buyer would describe the thing.
"""
import argparse
import math
import json
import os
import re
import sys
from collections import defaultdict

import openpyxl

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XLSX = os.path.join(ROOT, "ewe", "proizvodi_1787076117030.xlsx")
OUT = os.path.join(ROOT, "src", "data", "products.json")

AVAILABILITY = "Dostupnost i rok isporuke potvrđujemo uz ponudu"

# EWE kategorija -> shop category. Names describe what is actually in the feed:
# "Laptop računari i oprema" carries zero laptops at PMP, only bags and stands.
CATEGORY_MAP = {
    "Monitori i dodatna oprema": "Monitori",
    "Periferije": "Periferija",
    "Audio oprema": "Periferija",
    "Kablovi i adapteri": "Periferija",
    "Gaming oprema": "Periferija",
    "Čitači kartica": "Periferija",
    "Laptop računari i oprema": "Laptop oprema",
    "Tableti i oprema": "Tableti",
    "HDD i SSD": "Komponente",
    "Ram memorije": "Komponente",
    "Procesori": "Komponente",
    "Matične ploče": "Komponente",
    "Grafičke karte": "Komponente",
    "Kućišta i napajanja": "Komponente",
    "Eksterni SSD": "Komponente",
    "Eksterni HDD": "Komponente",
    "USB memorije": "Komponente",
    "Memorijske kartice": "Komponente",
    "Hlađenje": "Komponente",
    "Kontroleri/Kartice": "Komponente",
    "Optički uređaji": "Komponente",
}

CATEGORY_ORDER = ["Monitori", "Periferija", "Laptop oprema", "Tableti", "Komponente"]

TRANSLIT = str.maketrans(
    {"š": "s", "đ": "dj", "č": "c", "ć": "c", "ž": "z",
     "Š": "s", "Đ": "dj", "Č": "c", "Ć": "c", "Ž": "z"}
)

# Only these keys are read out of Opis. A whitelist beats a generic "Key: value"
# regex here — without it "Tip: Punjač za Apple uređaje Snaga: 20W" parses
# "Apple uređaje Snaga" as a key and truncates the value to "Punjač za".
SPEC_KEYS = [
    "Veličina ekrana", "Rezolucija", "Tip panela", "Pozadinsko osvetljenje",
    "Odnos stranica", "Nativni kontrast", "Osvetljenje", "Odziv", "Osvežavanje",
    "Tip", "Snaga", "Priključci", "Boja", "Upotreba", "Kapacitet", "Interfejs",
    "Procesor", "Interna memorija", "Operativni sistem", "Povezivanje",
    "Materijal", "Dimenzije", "Bežična veza", "Tehnologija",
]
SPEC_RE = re.compile(r"(?:^|\s)(" + "|".join(map(re.escape, SPEC_KEYS)) + r"):\s")


def num(value):
    """Accept Excel numbers, Serbian grouped amounts and decimal-dot exports."""
    if value is None or isinstance(value, bool) or str(value).strip() == "":
        return None
    if isinstance(value, (int, float)):
        return float(value) if math.isfinite(value) and value > 0 else None
    text = str(value).replace("RSD", "").replace("\xa0", "").replace(" ", "").strip()
    if "," in text:
        if not re.fullmatch(r"(?:\d+|\d{1,3}(?:\.\d{3})+),\d{1,2}", text):
            return None
        text = text.replace(".", "").replace(",", ".")
    elif re.fullmatch(r"\d{1,3}(?:\.\d{3})+", text):
        text = text.replace(".", "")
    elif not re.fullmatch(r"\d+(?:\.\d{1,2})?", text):
        return None
    try:
        parsed = float(text)
        return parsed if math.isfinite(parsed) and parsed > 0 else None
    except ValueError:
        return None


def round_90(price):
    """Nearest ...990 at 10.000+, nearest ...90 below."""
    target, step = (990, 1000) if price >= 10000 else (90, 100)
    base = (int(price) // step) * step + target
    return min((c for c in (base - step, base, base + step) if c > 0),
               key=lambda c: abs(c - price))


def slugify(text):
    text = text.translate(TRANSLIT).lower()
    return re.sub(r"-{2,}", "-", re.sub(r"[^a-z0-9]+", "-", text)).strip("-")[:70]


def parse_opis(opis):
    if not opis:
        return {}
    text = re.sub(r"\s+", " ", str(opis)).strip()
    matches = list(SPEC_RE.finditer(text))
    out = {}
    for i, match in enumerate(matches):
        key = match.group(1)
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        value = text[start:end].strip(" ,;")
        # The whitelist only marks where values START. A value still runs on into
        # the next "Masa:" / "Model:" / "Senzor:" pair, so cut at any further key.
        value = re.split(r"\s+[A-ZŠĐČĆŽ][A-Za-zšđčćžŠĐČĆŽ ]{0,28}:\s", value)[0]
        # Strip a trailing group heading such as "... Bela Miš -" or
        # "... Siva Reklamacioni period -" (headings can be several words).
        value = re.sub(
            r"\s+[A-ZŠĐČĆŽ][A-Za-zšđčćž]*(?:\s+[A-Za-zšđčćž]+){0,3}\s*-\s*$", "", value
        ).strip(" ,;-")
        value = re.sub(r",(?=\S)", ", ", value)
        if value and len(value) < 70 and key not in out:
            out[key] = value
    return out


def inches(name):
    """Screen size from the name. Two decimals ("11.97 inch" must not read as 97),
    and for a range like "14-16 inch" the upper bound is what a bag fits."""
    match = re.search(r"\b(\d{1,2}(?:[.,]\d{1,2})?)\s*(?:-\s*(\d{1,2}(?:[.,]\d{1,2})?))?\s*inch",
                      name, re.I)
    if not match:
        return None
    return (match.group(2) or match.group(1)).replace(",", ".")


def has(name, *words):
    low = name.lower()
    return any(w in low for w in words)


def layout(name):
    """Keyboard layout matters a lot to Serbian buyers — surface it."""
    if re.search(r"\bSRB CYR\b", name):
        return "srpski ćirilični raspored"
    if re.search(r"\bYU\b", name):
        return "YU raspored"
    if re.search(r"\bUS\b", name):
        return "US raspored"
    return None


def wireless(name):
    if has(name, "wireless", "bluetooth", "bežič", "rechargeable"):
        return "Bežič"
    if has(name, "wired", " usb"):
        return "Žičan"
    return None


def describe(name, brand, category, specs):
    """One plain Serbian sentence. Built from the name; specs only enrich it."""
    low = name.lower()
    conn = wireless(name)
    lay = layout(name)
    lay_part = f", {lay}" if lay else ""

    # --- Periferija -------------------------------------------------------
    if "tastatura" in low and "miš" in low:
        lead = {"Bežič": "Bežični", "Žičan": "Žičani"}.get(conn, "Komplet")
        return f"{lead} set tastature i miša{lay_part} — za svakodnevni rad za radnim stolom."

    if "tastatura" in low:
        lead = {"Bežič": "Bežična", "Žičan": "Žičana"}.get(conn, "Tastatura")
        noun = "tastatura" if lead != "Tastatura" else ""
        return f"{lead} {noun}{lay_part}".strip() + " — za svakodnevni rad za radnim stolom."

    if "miš" in low:
        lead = {"Bežič": "Bežični", "Žičan": "Žičani"}.get(conn, "Optički")
        sensor = "laserski" if "laser" in low else "optički"
        extra = ", tih rad" if "silent" in low else ""
        return f"{lead} {sensor} miš{extra} — za svakodnevni rad za radnim stolom."

    if has(low, "speakerphone", "spikerfon"):
        return "Konferencijski zvučnik sa mikrofonom — za sale za sastanke i onlajn pozive."

    if has(low, "headset", "slušalice", "earbuds"):
        anc = " sa aktivnim potiskivanjem buke" if "anc" in low else ""
        base = "Bežične bubice" if "earbuds" in low else "Slušalice sa mikrofonom"
        return f"{base}{anc} — za pozive i onlajn sastanke."

    if has(low, "power adapter", "punjač"):
        watt = re.search(r"(\d{2,3})\s*W", name)
        watt_part = f" od {watt.group(1)}W" if watt else ""
        return f"USB-C punjač{watt_part} — za dopunu laptopa i tableta na radnom mestu."

    # --- Laptop oprema ----------------------------------------------------
    if has(low, "ranac", "backpack"):
        size = inches(name)
        return f"Ranac za laptop{f' do {size} inča' if size else ''} — za svakodnevno nošenje."

    if has(low, "torba", "briefcase"):
        size = inches(name)
        return f"Torba za laptop{f' do {size} inča' if size else ''} — za svakodnevno nošenje."

    if has(low, "futrola", "sleeve"):
        size = inches(name)
        return f"Futrola za laptop{f' do {size} inča' if size else ''} — zaštita u rancu ili torbi."

    if has(low, "postolje", "ergostand", "hladnjak za laptop"):
        return "Postolje sa hlađenjem za laptop — za duži rad za stolom i bolju ergonomiju."

    if "hub" in low:
        ports = re.search(r"(\d+)-u-(\d+)", name)
        port_part = f" {ports.group(0)}" if ports else ""
        return f"USB-C hub{port_part} — monitor, mreža i periferija na jednom kablu."

    # --- Tableti ----------------------------------------------------------
    if category == "Tableti":
        if has(low, "nosač", "mount"):
            return "Zidni nosač za tablet — za montažu u lokalu, magacinu ili sali za sastanke."
        size = inches(name) or (pick(specs, "Veličina ekrana") or "").replace(" inča", "")
        storage = re.search(r"(\d+)GB\s+Android", name)
        mem = f" i {storage.group(1)}GB memorije" if storage else ""
        net = ", sa 4G" if "4g" in low else ""
        return f"Tablet od {size} inča{mem}{net} — za teren, magacin i prezentacije."

    # --- Komponente -------------------------------------------------------
    if "vodeno hlađenje" in low:
        size = re.search(r"\b(\d{3})\b", name)
        rad = f" sa {size.group(1)} mm radijatorom" if size else ""
        return f"Vodeno hlađenje procesora{rad} — za mašine pod stalnim opterećenjem."

    if "ventilator" in low:
        size = re.search(r"(\d{3})\s*mm", name)
        size_part = f" od {size.group(1)} mm" if size else ""
        return f"Ventilator za kućište{size_part} — za tiše i hladnije radne mašine."

    if "napajanje" in low:
        watt = re.search(r"(\d{3,4})\s*W", name)
        cert = re.search(r"80\s*PLUS\s+(\w+)", name, re.I)
        watt_part = f" od {watt.group(1)}W" if watt else ""
        cert_part = f", 80 PLUS {cert.group(1).capitalize()}" if cert else ""
        return f"Napajanje{watt_part}{cert_part} — za pouzdan rad kancelarijskih računara."

    if "kućište" in low:
        return "Kućište za desktop računar — za tihu mašinu na radnom stolu."

    # --- Monitori ---------------------------------------------------------
    if category == "Monitori":
        size = pick(specs, "Veličina ekrana") or (f"{inches(name)} inča" if inches(name) else None)
        panel = pick(specs, "Tip panela")
        res = pick(specs, "Rezolucija")
        if size and res:
            panel_part = f"{panel} panel i " if panel else ""
            return f"Monitor od {size}, {panel_part}rezolucija {res} — za svakodnevni rad u kancelariji."
        if size:
            return f"Monitor od {size} — za svakodnevni rad u kancelariji."

    return f"{brand.title()} — oprema za kancelarijske radne mašine."


def pick(specs, *names):
    for name in names:
        for key, value in specs.items():
            if key.lower() == name.lower():
                return value
    return None


def build_specs(specs, name, category):
    """Up to three short facts. Falls back to what the name itself states."""
    out = []
    wanted = {
        "Monitori": ["Veličina ekrana", "Rezolucija", "Tip panela"],
        "Periferija": ["Tip", "Povezivanje", "Boja"],
        "Laptop oprema": ["Materijal", "Boja", "Dimenzije"],
        "Tableti": ["Veličina ekrana", "Interna memorija", "Operativni sistem"],
        "Komponente": ["Tip", "Snaga", "Dimenzije"],
    }[category]
    for key in wanted:
        value = pick(specs, key)
        if value and f"{key}: {value}" not in out:
            out.append(f"{key}: {value}")

    if len(out) < 3:
        lay = layout(name)
        conn = wireless(name)
        size = inches(name)
        watt = re.search(r"(\d{3,4})\s*W\b", name)
        mm = re.search(r"(\d{3})\s*mm", name)
        storage = re.search(r"(\d+)GB\s+Android", name)
        android = re.search(r"Android\s+([\d.]+)", name)
        for extra in (
            lay,
            "Bežično povezivanje" if conn == "Bežič"
            else ("Žično povezivanje" if conn == "Žičan" else None),
            f"Za laptop do {size} inča" if size and category == "Laptop oprema" else None,
            f"Ekran {size} inča"
            if size and category == "Tableti"
            and not any(s.startswith("Veličina ekrana") for s in out) else None,
            f"Memorija {storage.group(1)}GB" if storage else None,
            f"Android {android.group(1)}" if android else None,
            "4G mobilni internet" if "4g" in name.lower() and category == "Tableti" else None,
            f"Snaga {watt.group(1)}W" if watt else None,
            f"Prečnik {mm.group(1)} mm" if mm and category == "Komponente" else None,
        ):
            if extra and extra not in out:
                out.append(extra)
    return out[:3]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=XLSX, help="Path to EWE XLSX export")
    args = parser.parse_args()
    with open(OUT, encoding="utf-8") as handle:
        existing = json.load(handle)
    for key in ('id', 'slug'):
        if len({p[key] for p in existing}) != len(existing):
            raise ValueError(f"Catalog contains duplicate {key} values; refresh aborted")
    selected = {p["supplier_sku"]: p for p in existing if p.get("auto_price") and p.get("supplier_sku")}
    workbook = openpyxl.load_workbook(args.input, read_only=True, data_only=True)
    sheet = workbook["ewe"]
    rows = sheet.iter_rows(values_only=True)
    header = next(rows)
    idx = {name: i for i, name in enumerate(header)}
    required = {"Ident", "PMP", "Kategorija", "Podkategorija", "Proizvođač", "Naziv", "Cena sa popustom", "Opis"}
    if not required.issubset(idx):
        raise ValueError("Export is missing required columns")

    items = {}
    for row in rows:
        if row is None or row[idx["Ident"]] is None:
            continue
        ident = str(row[idx["Ident"]]).strip()
        pmp = num(row[idx["PMP"]])
        if ident not in items:
            items[ident] = {
                "kat": row[idx["Kategorija"]],
                "sub": row[idx["Podkategorija"]],
                "brand": str(row[idx["Proizvođač"]] or "").strip(),
                "name": re.sub(r"\s+", " ", str(row[idx["Naziv"]] or "")).strip(),
                "buy": num(row[idx["Cena sa popustom"]]),
                "opis": row[idx["Opis"]],
                "pmp": pmp,
            }
        elif pmp and not items[ident]["pmp"]:
            items[ident]["pmp"] = pmp
    workbook.close()

    products, skipped = [], []
    for ident, item in items.items():
        category = CATEGORY_MAP.get(item["kat"])
        if ident not in selected or not category or not item["pmp"] or not item["name"]:
            continue

        price = round_90(item["pmp"] * 1.05)
        if item["buy"] and price < item["buy"]:
            skipped.append((ident, item["name"], price, item["buy"]))
            continue

        specs_map = parse_opis(item["opis"])
        slug = slugify(f"{item['brand']}-{item['name']}") or slugify(ident)

        product = {
            "id": slug,
            "slug": slug,
            "name": item["name"],
            "category": category,
            "brand": item["brand"],
            "short_desc": describe(item["name"], item["brand"], category, specs_map),
            "specs": build_specs(specs_map, item["name"], category),
            "price_rsd": price,
            "price_note": None,
            "image": None,
            "availability": AVAILABILITY,
            "featured": False,
            "supplier_sku": ident,
            "auto_price": True,
        }
        old = selected[ident]
        for key in ("id", "slug", "name", "category", "brand", "short_desc", "specs", "image", "featured"):
            product[key] = old[key]
        products.append(product)

    updated = {p["supplier_sku"]: p for p in products}
    products = []
    for old in existing:
        if not old.get("auto_price"):
            products.append(old)
        elif old.get("supplier_sku") in updated:
            products.append(updated[old["supplier_sku"]])
        else:
            products.append({**old, "price_rsd": None, "price_note": "Cena na upit", "availability": AVAILABILITY})

    by_category = defaultdict(list)
    for product in products:
        by_category[product["category"]].append(product)

    products.sort(key=lambda p: (not p["featured"], CATEGORY_ORDER.index(p["category"]) if p["category"] in CATEGORY_ORDER else len(CATEGORY_ORDER), p["name"]))

    with open(OUT + ".tmp", "w", encoding="utf-8") as handle:
        json.dump(products, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    os.replace(OUT + ".tmp", OUT)

    print(f"wrote {OUT}\n{len(products)} products")
    for category in CATEGORY_ORDER:
        print(f"  {len(by_category[category]):4d}  {category}")
    print(f"\nskipped (computed price below buy price): {len(skipped)}")
    for ident, name, price, buy in skipped:
        print(f"  {ident}  {name[:44]:46s} {price:>9,.0f} < {buy:>9,.0f}")

    print("\n=== sample short_desc ===")
    for category in CATEGORY_ORDER:
        print(f"\n{category}:")
        for product in [p for p in products if p["category"] == category][:4]:
            print(f"  {product['name'][:56]}")
            print(f"    -> {product['short_desc']}")
            print(f"       {product['specs']}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
