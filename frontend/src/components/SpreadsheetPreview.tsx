import { useEffect, useMemo, useState } from "react";

import type {
  ParsedSheet,
  SelectionState,
  TableRange,
} from "../types/excel";

import {
  columnLetter,
  coordinatesToRange,
  isCellInsideRange,
  isCellInsideSelection,
} from "../utils/range";

type SpreadsheetPreviewProps = {
  sheet: ParsedSheet;
  tables: TableRange[];
  selectingTableIndex: number | null;
  onRangeSelected: (
    range: string
  ) => void;
  onCancelSelection: () => void;
};

function SpreadsheetPreview({
  sheet,
  tables,
  selectingTableIndex,
  onRangeSelected,
  onCancelSelection,
}: SpreadsheetPreviewProps) {
  const [selection, setSelection] =
    useState<SelectionState | null>(null);

  const [isSelecting, setIsSelecting] =
    useState(false);

  const columnCount = useMemo(() => {
    return Math.max(
      ...sheet.data.map(
        (row) => row.length
      ),
      1
    );
  }, [sheet.data]);

  const isSelectionMode =
    selectingTableIndex !== null;

  useEffect(() => {
    if (!isSelectionMode) {
      setSelection(null);
      setIsSelecting(false);
    }
  }, [isSelectionMode]);

  useEffect(() => {
    function handleMouseUp() {
      if (!isSelecting) {
        return;
      }

      setIsSelecting(false);
    }

    window.addEventListener(
      "mouseup",
      handleMouseUp
    );

    return () => {
      window.removeEventListener(
        "mouseup",
        handleMouseUp
      );
    };
  }, [isSelecting]);

  function handleCellMouseDown(
    rowIndex: number,
    columnIndex: number
  ) {
    if (!isSelectionMode) {
      return;
    }

    const row = rowIndex + 1;
    const column = columnIndex + 1;

    setIsSelecting(true);

    setSelection({
      startRow: row,
      startColumn: column,
      endRow: row,
      endColumn: column,
    });
  }

  function handleCellMouseEnter(
    rowIndex: number,
    columnIndex: number
  ) {
    if (
      !isSelectionMode ||
      !isSelecting ||
      !selection
    ) {
      return;
    }

    setSelection({
      ...selection,
      endRow: rowIndex + 1,
      endColumn: columnIndex + 1,
    });
  }

  function confirmSelection() {
    if (!selection) {
      return;
    }

    const range =
      coordinatesToRange(selection);

    onRangeSelected(range);

    setSelection(null);
    setIsSelecting(false);
  }

  function getCellClassName(
    rowIndex: number,
    columnIndex: number
  ): string {
    const row = rowIndex + 1;
    const column = columnIndex + 1;

    const selectedByTable =
      tables.some((table) =>
        isCellInsideRange(
          row,
          column,
          table.range
        )
      );

    const selectedForEditing =
      isCellInsideSelection(
        row,
        column,
        selection
      );

    const classNames: string[] = [];

    if (selectedByTable) {
      classNames.push("selected-cell");
    }

    if (selectedForEditing) {
      classNames.push(
        "range-selection-cell"
      );
    }

    return classNames.join(" ");
  }

  return (
    <section className="sheet-card">
      <div className="section-header">
        <div>
          <p className="eyebrow">
            Workbook preview
          </p>

          <h2>{sheet.name}</h2>
        </div>

        <span className="sheet-info">
          {sheet.data.length} rows
        </span>
      </div>

      {isSelectionMode && (
        <div className="range-selection-banner">
          <div>
            <strong>
              Selecting range
              {selectingTableIndex !== null
                ? ` for Table ${
                    selectingTableIndex + 1
                  }`
                : ""}
            </strong>

            <span>
              Click and drag over the cells
              you want to use.
            </span>
          </div>

          <div className="range-selection-actions">
            <button
              className="button secondary-button"
              onClick={onCancelSelection}
            >
              Cancel
            </button>

            <button
              className="button primary-button"
              onClick={confirmSelection}
              disabled={!selection}
            >
              Use selected range
            </button>
          </div>
        </div>
      )}

      <div
        className={`spreadsheet-wrapper ${
          isSelectionMode
            ? "spreadsheet-selecting"
            : ""
        }`}
      >
        <table className="spreadsheet">
          <thead>
            <tr>
              <th className="corner-cell"></th>

              {Array.from(
                {
                  length: columnCount,
                },
                (_, index) => (
                  <th key={index}>
                    {columnLetter(index + 1)}
                  </th>
                )
              )}
            </tr>
          </thead>

          <tbody>
            {sheet.data.map(
              (row, rowIndex) => (
                <tr key={rowIndex}>
                  <th className="row-number">
                    {rowIndex + 1}
                  </th>

                  {Array.from(
                    {
                      length: columnCount,
                    },
                    (_, columnIndex) => {
                      const value =
                        row[columnIndex];

                      return (
                        <td
                          key={columnIndex}
                          className={getCellClassName(
                            rowIndex,
                            columnIndex
                          )}
                          onMouseDown={() =>
                            handleCellMouseDown(
                              rowIndex,
                              columnIndex
                            )
                          }
                          onMouseEnter={() =>
                            handleCellMouseEnter(
                              rowIndex,
                              columnIndex
                            )
                          }
                        >
                          {value instanceof Date
                            ? value.toLocaleDateString()
                            : value?.toString() ??
                              ""}
                        </td>
                      );
                    }
                  )}
                </tr>
              )
            )}
          </tbody>
        </table>
      </div>

      {tables.length > 0 &&
        !isSelectionMode && (
          <p className="preview-hint">
            Highlighted cells show the
            currently selected table ranges.
          </p>
        )}
    </section>
  );
}

export default SpreadsheetPreview;