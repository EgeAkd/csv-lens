"""Inspect CSV data locally and emit a JSON quality report."""
import argparse
import csv
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path


def profile(path, delimiter=','):
    with Path(path).open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.reader(handle, delimiter=delimiter, strict=True)
        headers = next(reader, None)
        if not headers or any(not h.strip() for h in headers):
            raise ValueError('A non-empty header is required for every column')
        if len(set(headers)) != len(headers):
            raise ValueError('Duplicate column names are not supported')
        columns = [{'name': h, 'missing': 0, 'numeric_count': 0, 'min': None, 'max': None} for h in headers]
        seen, rows, duplicates = set(), 0, 0
        for record in reader:
            if len(record) != len(headers):
                raise ValueError(f'CSV line {reader.line_num}: expected {len(headers)} fields, got {len(record)}')
            rows += 1
            key = tuple(record)
            duplicates += key in seen
            seen.add(key)
            for value, column in zip(record, columns):
                value = value.strip()
                if not value:
                    column['missing'] += 1
                    continue
                try:
                    number = Decimal(value)
                except InvalidOperation:
                    continue
                if not number.is_finite():
                    continue
                column['numeric_count'] += 1
                column['min'] = number if column['min'] is None else min(column['min'], number)
                column['max'] = number if column['max'] is None else max(column['max'], number)
        for column in columns:
            for bound in ('min', 'max'):
                if column[bound] is not None:
                    column[bound] = str(column[bound])
        return {'rows': rows, 'duplicate_rows': duplicates, 'columns': columns}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    parser.add_argument('--delimiter', default=',', help='Single-character separator, e.g. ;')
    args = parser.parse_args()
    if len(args.delimiter) != 1:
        parser.error('--delimiter must be one character')
    try:
        print(json.dumps(profile(args.file, args.delimiter), indent=2, ensure_ascii=False))
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(1, f'Error: {error}\n')


if __name__ == '__main__':
    main()
