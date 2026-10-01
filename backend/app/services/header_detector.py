import pandas as pd


def detect_header_row(
    table: pd.DataFrame,
) -> int:
    """
    Detect the header row.

    Current strategy:
    the first row containing at least one non-empty value
    is treated as the header.

    Returns:
        Zero-based row index.
    """

    for index, row in table.iterrows():

        if row.notna().any():
            return index

    raise ValueError(
        "No valid header row found in the table."
    )


def apply_header(
    table: pd.DataFrame,
) -> pd.DataFrame:
    """
    Detect and apply the header row.
    """

    header_row = detect_header_row(table)

    headers = table.iloc[header_row].tolist()

    headers = make_column_names_unique(
        headers
    )

    result = table.iloc[
        header_row + 1:
    ].copy()

    result.columns = headers

    return result.reset_index(drop=True)


def make_column_names_unique(
    columns,
) -> list[str]:
    """
    Make duplicate column names unique.

    Example:
        ["id", "name", "id"]
        ->
        ["id", "name", "id.1"]
    """

    seen = {}
    unique_columns = []

    for index, column in enumerate(columns):

        # Handle empty/NaN column names.
        if pd.isna(column):
            column = f"column_{index + 1}"
        else:
            column = str(column).strip()

            if not column:
                column = f"column_{index + 1}"

        if column in seen:
            seen[column] += 1
            unique_name = f"{column}.{seen[column]}"
        else:
            seen[column] = 0
            unique_name = column

        unique_columns.append(unique_name)

    return unique_columns