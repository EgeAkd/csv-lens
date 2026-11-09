# CSV Lens

**Understand a CSV file before you work with it.**

A dependency-free Python CLI that reports row counts, repeated rows, missing values and numeric ranges. Everything stays on your computer.

## Run it

Python 3.10 or newer; no installation or API key required.

```sh
git clone https://github.com/EgeAkd/csv-lens.git
cd csv-lens
python3 csv_lens.py examples/inventory.csv
python3 csv_lens.py your-file.csv --delimiter ';' > report.json
```

The included fictional inventory produces **5 rows**, **1 duplicate row** and **1 missing quantity**. See [the complete example report](examples/report.json).

## What it checks

| Check | Definition |
| --- | --- |
| Rows | Data records, excluding the header |
| Duplicate rows | Repeated occurrences beyond the first, matching every raw field |
| Missing | Empty or whitespace-only values |
| Numeric count | Finite decimal values in each column |
| Min / max | Numeric extrema, returned as strings to preserve decimal precision |

UTF-8 files with or without a BOM are supported. Quoted fields and embedded newlines follow Python's CSV reader. Duplicate or empty headers and inconsistent row widths fail with an error instead of silently dropping data. The input is never modified.

## Scope and limitations

This is a small local inspection tool, not a data cleaning engine. It does not infer dates, currencies or locale-specific decimal separators. `NaN` and infinity are non-numeric values, not missing values. Duplicate detection stores distinct rows in memory, so memory use grows with the input. Numeric bounds summarize numeric cells even in mixed-type columns. Use another tool for datasets that do not fit in memory.

## Development

```sh
python3 -m unittest discover -s tests -v
```

Tests cover missing data, duplicates, decimal precision, BOMs, quoted newlines, custom separators, invalid headers and malformed row widths. CI runs on Linux, macOS and Windows, with Python 3.10 and 3.12.

## Türkçe

CSV dosyalarını değiştirmeden satır sayısını, tekrarlanan kayıtları, eksik hücreleri ve sayısal aralıkları JSON olarak raporlar. Örnek dosyada gerçek müşteri veya işletme verisi bulunmaz.

## License

[MIT](LICENSE)
