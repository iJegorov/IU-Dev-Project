export type CellValue =
  | string
  | number
  | boolean
  | Date
  | null
  | undefined;

export type ParsedSheet = {
  name: string;
  data: CellValue[][];
};

export type TableRange = {
  name: string;
  range: string;
};

export type AnalyzeResponse = {
  filename: string;
  tables: TableRange[];
};

export type RangeCoordinates = {
  startRow: number;
  startColumn: number;
  endRow: number;
  endColumn: number;
};

export type SelectionState = {
  startRow: number;
  startColumn: number;
  endRow: number;
  endColumn: number;
};