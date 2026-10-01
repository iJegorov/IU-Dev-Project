import json

import pandas as pd

from app.services.json_exporter import (
    dataframe_to_records,
    export_table_to_json,
)


def test_dataframe_to_records():
    df = pd.DataFrame({
        "name": ["Alice", "Bob"],
        "age": [20, 25],
    })

    result = dataframe_to_records(df)

    assert result == [
        {
            "name": "Alice",
            "age": 20,
        },
        {
            "name": "Bob",
            "age": 25,
        },
    ]


def test_nan_values_become_none():
    df = pd.DataFrame({
        "name": ["Alice", None],
        "age": [20, None],
    })

    result = dataframe_to_records(df)

    assert result[1]["name"] is None
    assert result[1]["age"] is None


def test_export_table_to_json(tmp_path):
    df = pd.DataFrame({
        "name": ["Alice", "Bob"],
        "age": [20, 25],
    })

    output_path = export_table_to_json(
        df,
        tmp_path,
        "people.json",
    )

    assert output_path.exists()
    assert output_path.name == "people.json"

    with open(
        output_path,
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    assert data == [
        {
            "name": "Alice",
            "age": 20,
        },
        {
            "name": "Bob",
            "age": 25,
        },
    ]