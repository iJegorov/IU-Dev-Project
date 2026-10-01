from pathlib import Path

import pandas as pd


def read_excel_file(
    filepath: str | Path,
    sheet_name: int | str = 0,
) -> pd.DataFrame:
    """
    Read an Excel worksheet into a pandas DataFrame.

    header=None is intentional because we don't know the table headers
    before detecting the tables.
    """

    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(
            f"Excel file not found: {filepath}"
        )

    if filepath.suffix.lower() not in {".xlsx", ".xlsm"}:
        raise ValueError(
            "Unsupported file type. Please provide an XLSX or XLSM file."
        )

    return pd.read_excel(
        filepath,
        sheet_name=sheet_name,
        header=None,
    )