from alive_progress import alive_bar

import camelot
from camelot.core import Table, TableList

import multiprocessing

import pandas as pd

from pathlib import Path

import pickle

from typing import (
    Iterator,
    Sequence,
)


def extract_tables_from_pdf(pdf_path: Path) -> tuple[Path, TableList]:
    tables = camelot.read_pdf(
        str(pdf_path),
        pages = "all",
        flavor = "lattice",
        flag_size = True,
        table_areas = ["50,400,780,100"],
    )
    return pdf_path, tables


def process_pdf_directory(pdf_dir: Path) -> list[Table]:
    tables = []
    paths = list(pdf_dir.glob("*.pdf"))
    n_paths = len(paths)
    with multiprocessing.Pool(4) as pool:
        with alive_bar(title = "Parsing PDFs:", total = n_paths) as bar:
            for p, df_list in pool.imap_unordered(
                extract_tables_from_pdf,
                pdf_dir.glob("*.pdf"),
            ):
                tables.extend(df_list)
                bar()
                bar.text(f"Done with '{p.stem}', found {len(df_list)} table(s).")
    return tables


def save_tables(tables: list[str]) -> None:
    with open("tables.pkl", "wb") as f:
        pickle.dump(tables, f)


def main():
    pdf_dir = Path("pdf_data").resolve()
    # tables = process_pdf_directory(pdf_dir)
    _, tables = extract_tables_from_pdf(pdf_dir / "interim_report_february_2013.pdf")
    camelot.plot(tables[10], kind = "grid").show()
    breakpoint()
    # save_tables(tables)
    print(f"\nExtracted {len(tables)} total tables")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
