from dataclasses import dataclass


@dataclass
class TableRange:
    """
    Represents a rectangular table region in an Excel worksheet.

    Excel coordinates are 1-based:
    A1:C4 means rows 1-4 and columns A-C.
    """

    name: str
    start_row: int
    start_column: int
    end_row: int
    end_column: int

    def __post_init__(self):
        if self.start_row < 1 or self.end_row < 1:
            raise ValueError("Excel row numbers must be >= 1.")

        if self.start_column < 1 or self.end_column < 1:
            raise ValueError("Excel column numbers must be >= 1.")

        if self.start_row > self.end_row:
            raise ValueError("Start row cannot be greater than end row.")

        if self.start_column > self.end_column:
            raise ValueError("Start column cannot be greater than end column.")

    @property
    def range_string(self) -> str:
        """Return the range in Excel notation, e.g. A1:C4."""
        return (
            f"{number_to_column(self.start_column)}{self.start_row}:"
            f"{number_to_column(self.end_column)}{self.end_row}"
        )


def column_to_number(column: str) -> int:
    """
    Convert Excel column letters to a 1-based number.

    Examples:
        A  -> 1
        B  -> 2
        Z  -> 26
        AA -> 27
        AB -> 28
    """
    column = column.strip().upper()

    if not column.isalpha():
        raise ValueError(f"Invalid Excel column: {column}")

    result = 0

    for character in column:
        result = result * 26 + (ord(character) - ord("A") + 1)

    return result


def number_to_column(number: int) -> str:
    """Convert a 1-based column number to Excel letters."""
    if number < 1:
        raise ValueError("Column number must be >= 1.")

    result = ""

    while number > 0:
        number, remainder = divmod(number - 1, 26)
        result = chr(65 + remainder) + result

    return result


def parse_excel_range(
    range_string: str,
    name: str = "table"
) -> TableRange:
    """
    Convert an Excel range such as 'A1:C4' into a TableRange object.
    """

    import re

    pattern = r"^\s*([A-Za-z]+)(\d+)\s*:\s*([A-Za-z]+)(\d+)\s*$"

    match = re.match(pattern, range_string)

    if not match:
        raise ValueError(
            f"Invalid Excel range '{range_string}'. "
            "Expected format such as A1:C4."
        )

    start_column, start_row, end_column, end_row = match.groups()

    return TableRange(
        name=name,
        start_row=int(start_row),
        start_column=column_to_number(start_column),
        end_row=int(end_row),
        end_column=column_to_number(end_column),
    )