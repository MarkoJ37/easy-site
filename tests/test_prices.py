import importlib.util
from pathlib import Path
import unittest
import contextlib
import io
import json
import tempfile
from unittest.mock import patch
import openpyxl

spec = importlib.util.spec_from_file_location('prices', Path(__file__).parents[1] / 'scripts/seed-products.py')
prices = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prices)


class PriceTests(unittest.TestCase):
    def test_excel_and_export_formats(self):
        for value in [2490, 2490.0, '2490.00', '2.490,00', '2.490', '2 490,00 RSD']:
            with self.subTest(value=value):
                self.assertEqual(prices.num(value), 2490)

    def test_rejects_invalid_amounts(self):
        for value in [None, '', -1, 0, True, float('nan'), float('inf'), 'NaN', '1,2,3', '1.23.45']:
            with self.subTest(value=value):
                self.assertIsNone(prices.num(value))

    def test_decimal_amounts_are_not_multiplied(self):
        self.assertEqual(prices.num('2490.50'), 2490.5)
        self.assertEqual(prices.num('2.490,50'), 2490.5)

    def test_nearest_price_endings(self):
        for value, expected in [(2614.5, 2590), (10489, 9990), (10500, 10990), (18945, 18990)]:
            self.assertEqual(prices.round_90(value), expected)

    def test_refresh_keeps_manual_and_editorial_data_and_rejects_unselected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.title = 'ewe'
            sheet.append(['Ident', 'PMP', 'Kategorija', 'Podkategorija', 'Proizvođač', 'Naziv', 'Cena sa popustom', 'Opis'])
            for sku, pmp in [('chosen', 2490.0), ('unselected', 2490.0), ('too-cheap', 100.0)]:
                sheet.append([sku, pmp, 'Monitori i dodatna oprema', '', 'Brand', 'Supplier name', 2000, ''])
            workbook.save(root / 'feed.xlsx')
            base = dict(id='chosen', slug='chosen', name='Edited name', category='Monitori', brand='Brand',
                        short_desc='Edited description', specs=['Edited spec'], price_rsd=9990, price_note=None,
                        image='/custom.webp', availability='old', featured=True, supplier_sku='chosen', auto_price=True)
            manual = dict(base, id='manual', slug='manual', supplier_sku=None, auto_price=False, price_rsd=None, price_note='Cena na upit')
            missing = dict(base, id='missing', slug='missing', supplier_sku='missing')
            cheap = dict(base, id='too-cheap', slug='too-cheap', supplier_sku='too-cheap')
            output = root / 'products.json'
            output.write_text(json.dumps([base, manual, missing, cheap]), encoding='utf-8')
            with patch.object(prices, 'OUT', str(output)), patch('sys.argv', ['seed', '--input', str(root / 'feed.xlsx')]), contextlib.redirect_stdout(io.StringIO()):
                prices.main()
            result = {item['id']: item for item in json.loads(output.read_text(encoding='utf-8'))}
            self.assertEqual(set(result), {'chosen', 'manual', 'missing', 'too-cheap'})
            self.assertEqual(result['manual'], manual)
            self.assertEqual(result['chosen']['price_rsd'], 2590)
            self.assertEqual(result['chosen']['short_desc'], 'Edited description')
            self.assertEqual(result['chosen']['image'], '/custom.webp')
            self.assertIsNone(result['missing']['price_rsd'])
            self.assertIsNone(result['too-cheap']['price_rsd'])


if __name__ == '__main__':
    unittest.main()
