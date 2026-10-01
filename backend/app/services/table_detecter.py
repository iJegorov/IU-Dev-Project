from collections import deque

import numpy as np
import pandas as pd

from app.models.table_range import TableRange


def detect_table_ranges(df: pd.DataFrame) -> list[TableRange]:
    """
    Automatically detect tables based on connected non-empty cells.

    Empty rows and columns can separate different detected regions.

    Returns:
        A list of TableRange objects using Excel's 1-based coordinates.
    """

    if df.empty:
        return []

    non_empty_mask = ~df.isna()

    visited = np.zeros(
        (df.shape[0], df.shape[1]),
        dtype=bool,
    )

    tables = []

    for row in range(df.shape[0]):
        for column in range(df.shape[1]):

            if (
                non_empty_mask.iat[row, column]
                and not visited[row, column]
            ):
                table_range = _explore_table(
                    df,
                    non_empty_mask,
                    visited,
                    row,
                    column,
                    len(tables) + 1,
                )

                tables.append(table_range)

    return tables


def _explore_table(
    df: pd.DataFrame,
    non_empty_mask: pd.DataFrame,
    visited: np.ndarray,
    start_row: int,
    start_column: int,
    table_number: int,
) -> TableRange:
    """
    Find a connected region of non-empty cells using BFS.
    """

    queue = deque([(start_row, start_column)])

    visited[start_row, start_column] = True

    rows = []
    columns = []

    while queue:
        row, column = queue.popleft()

        rows.append(row)
        columns.append(column)

        neighbours = [
            (row - 1, column),
            (row + 1, column),
            (row, column - 1),
            (row, column + 1),
        ]

        for neighbour_row, neighbour_column in neighbours:

            if not (
                0 <= neighbour_row < df.shape[0]
                and 0 <= neighbour_column < df.shape[1]
            ):
                continue

            if (
                non_empty_mask.iat[
                    neighbour_row,
                    neighbour_column
                ]
                and not visited[
                    neighbour_row,
                    neighbour_column
                ]
            ):
                visited[
                    neighbour_row,
                    neighbour_column
                ] = True

                queue.append(
                    (neighbour_row, neighbour_column)
                )

    return TableRange(
        name=f"table_{table_number}",
        start_row=min(rows) + 1,
        start_column=min(columns) + 1,
        end_row=max(rows) + 1,
        end_column=max(columns) + 1,
    )