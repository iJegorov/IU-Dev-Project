import * as XLSX from "xlsx";

import type {
  CellValue,
  ParsedSheet,
} from "../types/excel";

export function isExcelFile(file: File): boolean {
  const extension = file.name
    .split(".")
    .pop()
    ?.toLowerCase();

  return (
    extension === "xlsx" ||
    extension === "xlsm"
  );
}

export async function parseExcelFile(
  file: File
): Promise<ParsedSheet> {
  const buffer = await file.arrayBuffer();

  const workbook = XLSX.read(buffer, {
    cellDates: true,
  });

  const firstSheetName = workbook.SheetNames[0];

  if (!firstSheetName) {
    throw new Error(
      "The workbook does not contain a worksheet."
    );
  }

  const worksheet =
    workbook.Sheets[firstSheetName];

  const worksheetRange = worksheet["!ref"];

  if (!worksheetRange) {
    throw new Error(
      "The worksheet does not contain any cells."
    );
  }

  const decodedRange =
    XLSX.utils.decode_range(worksheetRange);

  const data = XLSX.utils.sheet_to_json<CellValue[]>(
    worksheet,
    {
      header: 1,
      defval: null,
      range: {
        s: {
          r: 0,
          c: 0,
        },
        e: {
          r: decodedRange.e.r,
          c: decodedRange.e.c,
        },
      },
    }
  );

  return {
    name: firstSheetName,
    data,
  };
}