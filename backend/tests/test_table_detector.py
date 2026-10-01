import pandas as pd

from app.services.table_detecter import detect_table_ranges


def test_detect_single_table():
    df = pd.DataFrame([
        ["Name", "Age"],
        ["Alice", 20],
        ["Bob", 25],
    ])

    ranges = detect_table_ranges(df)

    assert len(ranges) == 1
    assert ranges[0].range_string == "A1:B3"


def test_detect_two_separate_tables():
    df = pd.DataFrame([
        ["Name", "Age", None, None],
        ["Alice", 20, None, None],
        ["Bob", 25, None, None],
        [None, None, None, None],
        [None, None, "Product", "Price"],
        [None, None, "Laptop", 1000],
    ])

    ranges = detect_table_ranges(df)

    assert len(ranges) == 2

    assert ranges[0].range_string == "A1:B3"
    assert ranges[1].range_string == "C5:D6"


def test_empty_dataframe_returns_no_tables():
    df = pd.DataFrame()

    ranges = detect_table_ranges(df)

    assert ranges == []


def test_table_names_are_generated():
    df = pd.DataFrame([
        ["A", "B"],
        [1, 2],
    ])

    ranges = detect_table_ranges(df)

    assert ranges[0].name == "table_1"