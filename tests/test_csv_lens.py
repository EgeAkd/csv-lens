import tempfile
import unittest
from pathlib import Path
from csv_lens import profile

class ProfileTests(unittest.TestCase):
    def report(self, text, delimiter=','):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'input.csv'
            path.write_text(text, encoding='utf-8')
            return profile(path, delimiter)

    def test_missing_duplicates_and_numeric_bounds(self):
        report = self.report('name,price\na,12.50\nb,\na,12.50\nc,-2\n')
        self.assertEqual(report['rows'], 4)
        self.assertEqual(report['duplicate_rows'], 1)
        self.assertEqual(report['columns'][1], {'name': 'price', 'missing': 1, 'numeric_count': 3, 'min': '-2', 'max': '12.50'})

    def test_bom_semicolon_and_quoted_newline(self):
        report = self.report('\ufeffname;value\n"two\nlines";3\n', ';')
        self.assertEqual(report['rows'], 1)
        self.assertEqual(report['columns'][0]['name'], 'name')

    def test_rejects_bad_shape_and_headers(self):
        for text in ['', 'a,a\n1,2\n', 'a,\n1,2\n', 'a,b\n1\n', 'a\n1,2\n']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                self.report(text)

    def test_nonfinite_is_not_numeric(self):
        report = self.report('x\nNaN\nInfinity\n2\n')
        self.assertEqual(report['columns'][0]['numeric_count'], 1)

    def test_header_only(self):
        self.assertEqual(self.report('a,b\n')['rows'], 0)

    def test_decimal_precision_preserved(self):
        report = self.report('x\n9007199254740993\n9007199254740992\n')
        self.assertEqual(report['columns'][0]['max'], '9007199254740993')

if __name__ == '__main__':
    unittest.main()
