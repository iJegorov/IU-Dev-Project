import pandas as pd

from app.services.header_detector import (
    apply_header,
    detect_header_row,
    make_column_names_unique,
)


def test_detect_header_row():
    df = pd.DataFrame([
        [None, None],
        ["Name", "Age"],
        ["Alice", 20],
    ])

    assert detect_header_row(df) == 1


def test_apply_header():
    df = pd.DataFrame([
        ["Name", "Age"],
        ["Alice", 20],
        ["Bob", 25],
    ])

    result = apply_header(df)

    expected = pd.DataFrame({
        "Name": ["Alice", "Bob"],
        "Age": [20, 25],
    })

    pd.testing.assert_frame_equal(
        result,
        expected,
        check_dtype=False,
    )


def test_duplicate_headers_are_made_unique():
    columns = [
        "id",
        "name",
        "id",
        "id",
    ]

    result = make_column_names_unique(columns)

    assert result == [
        "id",
        "name",
        "id.1",
        "id.2",
    ]


def test_empty_headers_receive_generated_names():
    columns = [
        "name",
        None,
        "",
    ]

    result = make_column_names_unique(columns)

    assert result == [
        "name",
        "column_2",
        "column_3",
    ]