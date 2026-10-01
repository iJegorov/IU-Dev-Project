import json

import pandas as pd

from app.models.table_range import TableRange
from app.xlsx_to_json import convert_excel_to_json


def create_test_excel_file(path):
    df = pd.DataFrame([
        ["Name", "Age", None, None],
        ["Alice", 20, None, None],
        ["Bob", 25, None, None],
        [None, None, None, None],
        [None, None, "Product", "Price"],
        [None, None, "Laptop", 1000],
        [None, None, "Phone", 500],
    ])

    df.to_excel(
        path,
        index=False,
        header=False,
    )


def test_convert_excel_to_json(tmp_path):
    input_file = tmp_path / "test.xlsx"
    output_directory = tmp_path / "output"

    create_test_excel_file(input_file)

    generated_files = convert_excel_to_json(
        input_file,
        output_directory,
    )

    assert len(generated_files) == 2

    assert (
        output_directory / "table_1.json"
    ).exists()

    assert (
        output_directory / "table_2.json"
    ).exists()


def test_user_ranges_override_automatic_detection(tmp_path):
    input_file = tmp_path / "test.xlsx"
    output_directory = tmp_path / "output"

    create_test_excel_file(input_file)

    user_ranges = [
        TableRange(
            name="people",
            start_row=1,
            start_column=1,
            end_row=3,
            end_column=2,
        )
    ]

    generated_files = convert_excel_to_json(
        input_file,
        output_directory,
        user_ranges=user_ranges,
    )

    assert len(generated_files) == 1

    assert (
        output_directory / "people.json"
    ).exists()

    with open(
        output_directory / "people.json",
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    assert data == [
        {
            "Name": "Alice",
            "Age": 20,
        },
        {
            "Name": "Bob",
            "Age": 25,
        },
    ]