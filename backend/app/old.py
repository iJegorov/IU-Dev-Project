import pandas as pd
import numpy as np
import json
import os




def split_excel_into_json_tables(excel_filepath, output_directory):
    """
    Splits a single Excel sheet with multiple tables separated by blank rows or blank columns into separate JSON files.

    Parameters:
        excel_filepath (str): Path to the Excel file.
        output_directory (str): Directory to save the JSON files.
    """
    # Load the entire sheet as a DataFrame
    df = pd.read_excel(excel_filepath, sheet_name=0, header=None)
    
    # Ensure output directory exists
    os.makedirs(output_directory, exist_ok=True)
    
    # Create a mask to identify non-empty cells
    non_empty_mask = ~df.isnull()
    
    # Initialize variables for tracking tables
    tables = []
    visited = np.zeros_like(non_empty_mask, dtype=bool)

    # Function to explore a table region
    def explore_table(start_row, start_col):
        queue = [(start_row, start_col)]
        visited[start_row, start_col] = True
        rows, cols = set(), set()

        while queue:
            row, col = queue.pop(0)
            rows.add(row)
            cols.add(col)

            for move_row, move_column in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor_row, neighbor_column = row + move_row, col + move_column
                if 0 <= neighbor_row < df.shape[0] and 0 <= neighbor_column < df.shape[1]:
                    if non_empty_mask.iat[neighbor_row, neighbor_column] and not visited[neighbor_row, neighbor_column]:
                        visited[neighbor_row, neighbor_column] = True
                        queue.append((neighbor_row, neighbor_column))

        rows = sorted(rows)
        cols = sorted(cols)
        table_region = df.iloc[rows, cols].reset_index(drop=True)
        return table_region

    # Iterate through the DataFrame to find tables
    for row in range(df.shape[0]):
        for col in range(df.shape[1]):
            if non_empty_mask.iat[row, col] and not visited[row, col]:
                table = explore_table(row, col)
                tables.append(table)

    # Process each table and save as JSON
    for i, table in enumerate(tables, start=1):
        table = table.dropna(axis=0, how="all").dropna(axis=1, how="all")

        # Detect header row
        header_row = detect_header_row(table)

        # Assign column names based on the detected header row
        table.columns = table.iloc[header_row]
        table.columns = make_column_names_unique(table.columns)  # Ensure unique column names
        table = table[header_row + 1:].reset_index(drop=True)

        # Convert table to JSON
        data_json = table.to_json(orient="records")
        data = json.loads(data_json)

        # Save to JSON file
        output_filepath = os.path.join(output_directory, f"table_{i}.json")
        with open(output_filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print(f"Table {i} saved to {output_filepath}")




def detect_header_row(data_frame):
    """
    Detects the header row index for a given DataFrame.
    """
    for index, row in data_frame.iterrows():
        if row.notnull().any():
            return index
    raise ValueError("No valid header row found in the DataFrame.")




def make_column_names_unique(columns):
    """
    Renames duplicate column names by appending a numerical suffix.
    Example: ["id", "id", "name"] -> ["id", "id.1", "name"]
    """
    seen = {}
    unique_columns = []

    for col in columns:
        if col in seen:
            seen[col] += 1
            unique_columns.append(f"{col}.{seen[col]}")  # Adding .1, .2, etc.
        else:
            seen[col] = 0
            unique_columns.append(col)

    return unique_columns
