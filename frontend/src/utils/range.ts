import type {
  RangeCoordinates,
  SelectionState,
} from "../types/excel";

export function columnToNumber(column: string): number {
  let result = 0;

  for (const character of column.toUpperCase()) {
    result =
      result * 26 +
      character.charCodeAt(0) -
      "A".charCodeAt(0) +
      1;
  }

  return result;
}

export function columnLetter(number: number): string {
  let result = "";

  while (number > 0) {
    const remainder = (number - 1) % 26;

    result =
      String.fromCharCode(65 + remainder) + result;

    number = Math.floor((number - 1) / 26);
  }

  return result;
}

export function parseRange(
  range: string
): RangeCoordinates | null {
  const match = range
    .trim()
    .match(/^([A-Za-z]+)(\d+):([A-Za-z]+)(\d+)$/);

  if (!match) {
    return null;
  }

  const startColumn = columnToNumber(match[1]);
  const startRow = Number(match[2]);
  const endColumn = columnToNumber(match[3]);
  const endRow = Number(match[4]);

  if (
    startRow > endRow ||
    startColumn > endColumn
  ) {
    return null;
  }

  return {
    startColumn,
    startRow,
    endColumn,
    endRow,
  };
}

export function coordinatesToRange(
  selection: SelectionState
): string {
  const startRow = Math.min(
    selection.startRow,
    selection.endRow
  );

  const endRow = Math.max(
    selection.startRow,
    selection.endRow
  );

  const startColumn = Math.min(
    selection.startColumn,
    selection.endColumn
  );

  const endColumn = Math.max(
    selection.startColumn,
    selection.endColumn
  );

  return `${columnLetter(startColumn)}${startRow}:${columnLetter(
    endColumn
  )}${endRow}`;
}

export function isCellInsideRange(
  row: number,
  column: number,
  range: string
): boolean {
  const parsed = parseRange(range);

  if (!parsed) {
    return false;
  }

  return (
    row >= parsed.startRow &&
    row <= parsed.endRow &&
    column >= parsed.startColumn &&
    column <= parsed.endColumn
  );
}

export function isCellInsideSelection(
  row: number,
  column: number,
  selection: SelectionState | null
): boolean {
  if (!selection) {
    return false;
  }

  const startRow = Math.min(
    selection.startRow,
    selection.endRow
  );

  const endRow = Math.max(
    selection.startRow,
    selection.endRow
  );

  const startColumn = Math.min(
    selection.startColumn,
    selection.endColumn
  );

  const endColumn = Math.max(
    selection.startColumn,
    selection.endColumn
  );

  return (
    row >= startRow &&
    row <= endRow &&
    column >= startColumn &&
    column <= endColumn
  );
}