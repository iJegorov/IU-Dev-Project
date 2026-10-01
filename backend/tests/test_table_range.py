import pytest

from app.models.table_range import (
    TableRange,
    column_to_number,
    number_to_column,
    parse_excel_range,
)


def test_column_to_number():
    assert column_to_number("A") == 1
    assert column_to_number("Z") == 26
    assert column_to_number("AA") == 27
    assert column_to_number("AB") == 28


def test_number_to_column():
    assert number_to_column(1) == "A"
    assert number_to_column(26) == "Z"
    assert number_to_column(27) == "AA"
    assert number_to_column(28) == "AB"


def test_column_conversion_is_reversible():
    for number in [1, 5, 26, 27, 52, 53, 100]:
        column = number_to_column(number)
        assert column_to_number(column) == number


def test_table_range_creates_correct_range_string():
    table_range = TableRange(
        name="products",
        start_row=1,
        start_column=1,
        end_row=4,
        end_column=3,
    )

    assert table_range.range_string == "A1:C4"


def test_parse_excel_range():
    table_range = parse_excel_range(
        "A1:C4",
        name="products",
    )

    assert table_range.name == "products"
    assert table_range.start_row == 1
    assert table_range.start_column == 1
    assert table_range.end_row == 4
    assert table_range.end_column == 3
    assert table_range.range_string == "A1:C4"


def test_parse_excel_range_with_spaces():
    table_range = parse_excel_range(
        "  B2 : D10  ",
        name="test",
    )

    assert table_range.range_string == "B2:D10"


def test_invalid_excel_range_raises_error():
    with pytest.raises(ValueError):
        parse_excel_range("invalid")


def test_invalid_table_range_coordinates():
    with pytest.raises(ValueError):
        TableRange(
            name="invalid",
            start_row=5,
            start_column=1,
            end_row=2,
            end_column=3,
        )