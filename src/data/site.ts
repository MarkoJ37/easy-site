/**
 * Single source of truth for everything that appears in more than one place.
 * Nothing here may be duplicated as a literal in a component.
 */

export const site = {
  brand: 'Easy Computers',
  legalName: 'Easy Computers J2M d.o.o.',
  url: 'https://easy.rs',
  founded: 1999,

  tel: '+381 63 1111727',
  telHref: 'tel:+381631111727',
  email: 'office@easy.rs',
  emailHref: 'mailto:office@easy.rs',

  // {VIBER_LINK} — the last open placeholder. Kept grep-able per CLAUDE.md §0.
  // The Kontakt component must hide the Viber/WhatsApp link while this is unset.
  viberLink: import.meta.env.PUBLIC_VIBER_LINK || '{VIBER_LINK}',

  pib: '102699654',
  mb: '17458795',

  address: {
    street: 'Veljka Petrovića 67',
    postalCode: '11030',
    city: 'Beograd',
    countryCode: 'RS',
  },

  // Radno vreme — matches the paketi's "remote podrška (pon–pet 9–17)".
  hours: 'Ponedeljak–petak, 09–17h',
  openingHoursSpec: 'Mo-Fr 09:00-17:00',

  meta: {
    title: 'Easy Computers — IT oprema i podrška za firme | Beograd',
    description:
      'Održavanje računara, nabavka opreme, Microsoft 365 i prelazak na Windows 11 za mala preduzeća. Besplatan IT pregled. Beograd i cela Srbija.',
  },
} as const;

export const addressLine = `${site.address.street}, ${site.address.postalCode} ${site.address.city}`;

/** Footer legal line — one string, used once, defined here so it stays consistent. */
export const legalLine = `${site.legalName} · PIB ${site.pib} · MB ${site.mb} · ${addressLine}`;

/** true once Marko replaces the token, so components can conditionally render. */
export const hasViber = !site.viberLink.startsWith('{');

export const cfBeaconToken = import.meta.env.PUBLIC_CF_BEACON_TOKEN || '';
export const analyticsEnabled = /^[a-f0-9]{32}$/i.test(cfBeaconToken);

/**
 * 18990 -> "18.990" — Serbian thousands separator, used for every price on /shop.
 * Done by hand rather than toLocaleString: the build machine's ICU data decides
 * whether sr-RS yields "18.990" or "18 990" with a narrow no-break space, and a
 * price must not change depending on where the site was built.
 */
export function formatRsd(value: number): string {
  return String(Math.round(value)).replace(/\B(?=(\d{3})+(?!\d))/g, '.');
}
