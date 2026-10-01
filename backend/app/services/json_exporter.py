import json
from pathlib import Path

import pandas as pd


def dataframe_to_records(
    table: pd.DataFrame,
) -> list[dict]:
    """
    Convert a DataFrame into a list of JSON-compatible records.
    """

    # Replace pandas NaN with None.
    table = table.where(
        pd.notna(table),
        None,
    )

    records = table.to_dict(
        orient="records"
    )

    return records


def export_table_to_json(
    table: pd.DataFrame,
    output_directory: str | Path,
    filename: str,
) -> Path:
    """
    Export a DataFrame as formatted JSON.

    Returns:
        Path to the generated JSON file.
    """

    output_directory = Path(
        output_directory
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        output_directory / filename
    )

    records = dataframe_to_records(table)

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            records,
            file,
            ensure_ascii=False,
            indent=4,
            default=str,
        )

    return output_path