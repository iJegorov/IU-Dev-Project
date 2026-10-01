from pathlib import Path

import pandas as pd

from app.models.table_range import TableRange
from app.services.excel_reader import read_excel_file
from app.services.header_detector import apply_header
from app.services.json_exporter import export_table_to_json
from app.services.table_detecter import detect_table_ranges
from app.services.table_extractor import extract_table


def analyze_excel(
    excel_filepath: str | Path,
) -> list[TableRange]:
    """
    Analyze an Excel file and automatically detect table ranges.

    This does not create JSON files.
    It only provides suggested table ranges.
    """

    df = read_excel_file(
        excel_filepath
    )

    return detect_table_ranges(df)


def convert_excel_to_json(
    excel_filepath: str | Path,
    output_directory: str | Path,
    user_ranges: list[TableRange] | None = None,
) -> list[Path]:
    """
    Convert tables in an Excel file to JSON.

    If user_ranges are provided, they completely override
    automatic table detection.

    If user_ranges is None, the application automatically
    detects table ranges.
    """

    df = read_excel_file(
        excel_filepath
    )

    # User-defined ranges override automatic detection.
    if user_ranges is not None:
        table_ranges = user_ranges
    else:
        table_ranges = detect_table_ranges(df)

    generated_files = []

    for table_range in table_ranges:

        table = extract_table(
            df,
            table_range,
            remove_empty=True,
        )

        if table.empty:
            continue

        table = apply_header(table)

        filename = (
            f"{table_range.name}.json"
        )

        output_path = export_table_to_json(
            table,
            output_directory,
            filename,
        )

        generated_files.append(
            output_path
        )

    return generated_files