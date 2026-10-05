import { useState } from "react";

import "./App.css";

import FileUpload from "./components/FileUpload";
import ErrorMessage from "./components/ErrorMessage";
import SpreadsheetPreview from "./components/SpreadsheetPreview";
import TableList from "./components/TableList";

import {
  analyzeWorkbook,
  convertWorkbook,
} from "./services/api";

import {
  isExcelFile,
  parseExcelFile,
} from "./utils/excel";

import type {
  ParsedSheet,
  TableRange,
} from "./types/excel";

function App() {
  const [file, setFile] =
    useState<File | null>(null);

  const [tables, setTables] =
    useState<TableRange[]>([]);

  const [sheet, setSheet] =
    useState<ParsedSheet | null>(null);

  const [loading, setLoading] =
    useState(false);

  const [converting, setConverting] =
    useState(false);

  const [error, setError] =
    useState("");

  const [selectingTableIndex, setSelectingTableIndex] =
    useState<number | null>(null);

  async function handleFileSelected(
    selectedFile: File
  ) {
    if (!isExcelFile(selectedFile)) {
      setError(
        "Please select an XLSX or XLSM file."
      );

      return;
    }

    setFile(selectedFile);
    setTables([]);
    setError("");
    setSelectingTableIndex(null);
    setLoading(true);

    try {
      // Parse the workbook for the spreadsheet preview
      const parsedSheet =
        await parseExcelFile(selectedFile);

      setSheet(parsedSheet);

      // Immediately analyze the workbook
      const response =
        await analyzeWorkbook(selectedFile);

      setTables(response.tables);
    } catch (error) {
      setSheet(null);
      setTables([]);

      setError(
        error instanceof Error
          ? error.message
          : "Could not analyze the Excel workbook."
      );
    } finally {
      setLoading(false);
    }
  }

  function updateTable(
    index: number,
    field: "name" | "range",
    value: string
  ) {
    setTables((currentTables) =>
      currentTables.map(
        (table, tableIndex) =>
          tableIndex === index
            ? {
                ...table,
                [field]: value,
              }
            : table
      )
    );
  }

  function addTable() {
    setTables((currentTables) => [
      ...currentTables,
      {
        name: `table_${
          currentTables.length + 1
        }`,
        range: "A1:B2",
      },
    ]);
  }

  function deleteTable(index: number) {
    setTables((currentTables) =>
      currentTables.filter(
        (_, tableIndex) =>
          tableIndex !== index
      )
    );

    if (
      selectingTableIndex === index
    ) {
      setSelectingTableIndex(null);
    }
  }

  function startRangeSelection(
    index: number
  ) {
    setSelectingTableIndex(index);
    setError("");
  }

  function cancelRangeSelection() {
    setSelectingTableIndex(null);
  }

  function handleRangeSelected(
    range: string
  ) {
    if (selectingTableIndex === null) {
      return;
    }

    updateTable(
      selectingTableIndex,
      "range",
      range
    );

    setSelectingTableIndex(null);
  }

  async function handleConvert() {
    if (!file) {
      setError(
        "Please select an Excel file first."
      );

      return;
    }

    if (tables.length === 0) {
      setError(
        "Please add at least one table."
      );

      return;
    }

    const invalidTable =
      tables.find(
        (table) =>
          !table.name.trim() ||
          !table.range.trim()
      );

    if (invalidTable) {
      setError(
        "Every table must have a name and a range."
      );

      return;
    }

    setConverting(true);
    setError("");

    try {
      const blob =
        await convertWorkbook(
          file,
          tables
        );

      const downloadUrl =
        window.URL.createObjectURL(blob);

      const link =
        document.createElement("a");

      link.href = downloadUrl;
      link.download =
        "converted_json.zip";

      document.body.appendChild(link);

      link.click();

      link.remove();

      window.URL.revokeObjectURL(
        downloadUrl
      );
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Something went wrong."
      );
    } finally {
      setConverting(false);
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <div>
          <p className="eyebrow">
            Spreadsheet utility
          </p>

          <h1>XLSX → JSON</h1>

          <p className="subtitle">
            Detect tables in an Excel workbook,
            review the ranges, and export them
            as separate JSON files.
          </p>
        </div>
      </header>

      <main className="workspace">
        <FileUpload
          file={file}
          loading={loading}
          onFileSelected={
            handleFileSelected
          }
        />

        <ErrorMessage message={error} />

        {sheet && (
          <SpreadsheetPreview
            sheet={sheet}
            tables={tables}
            selectingTableIndex={
              selectingTableIndex
            }
            onRangeSelected={
              handleRangeSelected
            }
            onCancelSelection={
              cancelRangeSelection
            }
          />
        )}

        {tables.length > 0 && (
          <TableList
            tables={tables}
            selectingTableIndex={
              selectingTableIndex
            }
            onUpdateTable={
              updateTable
            }
            onAddTable={addTable}
            onDeleteTable={
              deleteTable
            }
            onSelectRange={
              startRangeSelection
            }
            onConvert={handleConvert}
            converting={converting}
          />
        )}
      </main>
    </div>
  );
}

export default App;