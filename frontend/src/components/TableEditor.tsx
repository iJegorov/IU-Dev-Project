import Button from "./Button";

import type { TableRange } from "../types/excel";

import { parseRange } from "../utils/range";

type TableEditorProps = {
  table: TableRange;
  index: number;
  isSelecting: boolean;
  onUpdate: (
    field: "name" | "range",
    value: string
  ) => void;
  onDelete: () => void;
  onSelectRange: () => void;
};

function TableEditor({
  table,
  index,
  isSelecting,
  onUpdate,
  onDelete,
  onSelectRange,
}: TableEditorProps) {
  const validRange =
    parseRange(table.range) !== null;

  return (
    <article className="table-editor">
      <div className="table-editor-number">
        {index + 1}
      </div>

      <div className="table-editor-content">
        <label>
          <span>Table name</span>

          <input
            type="text"
            value={table.name}
            onChange={(event) =>
              onUpdate(
                "name",
                event.target.value
              )
            }
          />
        </label>

        <label>
          <span>Excel range</span>

          <div className="range-input-group">
            <input
              className={
                validRange
                  ? ""
                  : "input-invalid"
              }
              type="text"
              value={table.range}
              onChange={(event) =>
                onUpdate(
                  "range",
                  event.target.value
                )
              }
              placeholder="A1:B10"
            />

            <Button
              type="button"
              variant={
                isSelecting
                  ? "primary"
                  : "secondary"
              }
              onClick={onSelectRange}
            >
              {isSelecting
                ? "Selecting..."
                : "Select range"}
            </Button>
          </div>
        </label>
      </div>

      <button
        className="icon-button danger"
        onClick={onDelete}
        title="Delete table"
        type="button"
      >
        ×
      </button>
    </article>
  );
}

export default TableEditor;