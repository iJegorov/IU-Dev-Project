from pathlib import Path

from app.models.table_range import parse_excel_range
from app.xlsx_to_json import (
    analyze_excel,
    convert_excel_to_json,
)


BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = (
    BASE_DIR
    / "IO"
    / "input"
    / "4_test.xlsx"
)

OUTPUT_DIRECTORY = (
    BASE_DIR
    / "IO"
    / "output"
)


def main():
    print("Analyzing Excel file...")
    print(f"File: {INPUT_FILE}")
    print()

    # ----------------------------------------
    # 1. Automatic table detection
    # ----------------------------------------

    detected_ranges = analyze_excel(
        INPUT_FILE
    )

    print("Detected tables:")

    for table_range in detected_ranges:
        print(
            f"  {table_range.name}: "
            f"{table_range.range_string}"
        )

    print()

    # ----------------------------------------
    # 2. Example user-defined ranges
    # ----------------------------------------

    # Set this to None to use automatic detection.
    # user_ranges = None

    # Example:
    
    user_ranges = [
        parse_excel_range(
            "C4:H17",
            name="products",
        ),
        parse_excel_range(
            "K5:M8",
            name="accessories",
        ),
    ]

    # ----------------------------------------
    # 3. Convert
    # ----------------------------------------

    generated_files = convert_excel_to_json(
        INPUT_FILE,
        OUTPUT_DIRECTORY,
        user_ranges=user_ranges,
    )

    print("Generated files:")

    for filepath in generated_files:
        print(f"  {filepath}")


if __name__ == "__main__":
    main()