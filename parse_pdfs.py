import camelot

import pandas as pd

from pathlib import Path

from typing import Iterator


def extract_tables_from_pdf(pdf_path: Path) -> Iterator[pd.DataFrame]:
    tables = camelot.read_pdf(
        str(pdf_path),
        pages = "all",
        flavor = "lattice",
    )
    print(f"Found {len(tables)} tables in {pdf_path.name}")
    yield from (table.df for table in tables)


def process_pdf_directory(pdf_dir: Path) -> Iterator[pd.DataFrame]:
    results = {}
    
    for pdf_path in pdf_dir.glob("*.pdf"):
        yield from extract_tables_from_pdf(pdf_path)


def main():
    pdf_dir = Path("pdf_data").resolve()
    results = process_pdf_directory(pdf_dir)
    pdf_tables = next(results)
    
    # print(f"\nProcessed {len(results)} PDF files")
    # for pdf_name, tables in results.items():
    #     print(f"{pdf_name}: {len(tables)} tables")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
