import numpy as np
import pandas as pd

from app.models.table_range import TableRange


def extract_table(
    df: pd.DataFrame,
    table_range: TableRange,
    remove_empty: bool = True,
) -> pd.DataFrame:
    """
    Extract a rectangular region from a worksheet.

    TableRange uses 1-based Excel coordinates.
    pandas uses 0-based coordinates, so conversion happens here.
    """

    start_row = table_range.start_row - 1
    end_row = table_range.end_row

    start_column = table_range.start_column - 1
    end_column = table_range.end_column

    table = df.iloc[
        start_row:end_row,
        start_column:end_column,
    ].copy()

    if remove_empty:
        table = remove_empty_rows_and_columns(table)

    return table.reset_index(drop=True)


def remove_empty_rows_and_columns(
    table: pd.DataFrame,
) -> pd.DataFrame:
    """
    Remove rows and columns that contain only empty values
    or whitespace.
    """

    table = table.copy()

    # Convert whitespace-only strings into empty values.
    table = table.map(
        lambda value: (
            value.strip()
            if isinstance(value, str)
            else value
        )
    )

    table = table.replace("", np.nan)

    # Remove completely empty rows.
    table = table.dropna(
        axis=0,
        how="all",
    )

    # Remove completely empty columns.
    table = table.dropna(
        axis=1,
        how="all",
    )

    # Reset both row and column indexes.
    table = table.reset_index(drop=True)
    table.columns = range(table.shape[1])

    return table