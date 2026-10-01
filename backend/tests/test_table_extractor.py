import pandas as pd

from app.models.table_range import TableRange
from app.services.table_extractor import (
    extract_table,
    remove_empty_rows_and_columns,
)


def test_extract_table():
    df = pd.DataFrame([
        ["outside", None, None, None],
        [None, "Name", "Age", None],
        [None, "Alice", 20, None],
        [None, "Bob", 25, None],
        ["outside", None, None, None],
    ])

    table_range = TableRange(
        name="people",
        start_row=2,
        start_column=2,
        end_row=4,
        end_column=3,
    )

    result = extract_table(df, table_range)

    expected = pd.DataFrame([
        ["Name", "Age"],
        ["Alice", 20],
        ["Bob", 25],
    ])

    pd.testing.assert_frame_equal(
        result,
        expected,
    )


def test_empty_rows_are_removed():
    df = pd.DataFrame([
        ["Name", "Age"],
        [None, None],
        ["Alice", 20],
    ])

    result = remove_empty_rows_and_columns(df)

    expected = pd.DataFrame([
        ["Name", "Age"],
        ["Alice", 20],
    ])

    pd.testing.assert_frame_equal(
        result,
        expected,
    )


def test_empty_columns_are_removed():
    df = pd.DataFrame([
        ["Name", None, "Age"],
        ["Alice", None, 20],
        ["Bob", None, 25],
    ])

    result = remove_empty_rows_and_columns(df)

    expected = pd.DataFrame([
        ["Name", "Age"],
        ["Alice", 20],
        ["Bob", 25],
    ])

    pd.testing.assert_frame_equal(
        result,
        expected,
    )


def test_whitespace_is_treated_as_empty():
    df = pd.DataFrame([
        ["Name", "   ", "Age"],
        ["Alice", "   ", 20],
        ["Bob", "   ", 25],
    ])

    result = remove_empty_rows_and_columns(df)

    expected = pd.DataFrame([
        ["Name", "Age"],
        ["Alice", 20],
        ["Bob", 25],
    ])

    pd.testing.assert_frame_equal(
        result,
        expected,
    )


def test_empty_rows_and_columns_inside_user_range_are_removed():
    df = pd.DataFrame([
        ["Name", None, "Age", None],
        ["Alice", None, 20, None],
        [None, None, None, None],
        ["Bob", None, 25, None],
    ])

    table_range = TableRange(
        name="people",
        start_row=1,
        start_column=1,
        end_row=4,
        end_column=3,
    )

    result = extract_table(
        df,
        table_range,
        remove_empty=True,
    )

    expected = pd.DataFrame([
        ["Name", "Age"],
        ["Alice", 20],
        ["Bob", 25],
    ])

    pd.testing.assert_frame_equal(
        result,
        expected,
    )