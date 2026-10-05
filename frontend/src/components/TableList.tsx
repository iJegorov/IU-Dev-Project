import Button from "./Button";
import TableEditor from "./TableEditor";

import type { TableRange } from "../types/excel";

type TableListProps = {
  tables: TableRange[];
  selectingTableIndex: number | null;
  onUpdateTable: (
    index: number,
    field: "name" | "range",
    value: string
  ) => void;
  onAddTable: () => void;
  onDeleteTable: (index: number) => void;

  // The important correction:
  onSelectRange: (index: number) => void;

  onConvert: () => void;
  converting: boolean;
};

function TableList({
  tables,
  selectingTableIndex,
  onUpdateTable,
  onAddTable,
  onDeleteTable,
  onSelectRange,
  onConvert,
  converting,
}: TableListProps) {
  return (
    <section className="tables-section">
      <div className="section-header">
        <div>
          <p className="eyebrow">
            Review detected tables
          </p>

          <h2>Table ranges</h2>
        </div>

        <span className="table-count">
          {tables.length}{" "}
          {tables.length === 1
            ? "table"
            : "tables"}
        </span>
      </div>

      <div className="table-list">
        {tables.map((table, index) => (
          <TableEditor
            key={index}
            table={table}
            index={index}
            isSelecting={
              selectingTableIndex === index
            }
            onUpdate={(field, value) =>
              onUpdateTable(
                index,
                field,
                value
              )
            }
            onDelete={() =>
              onDeleteTable(index)
            }
            onSelectRange={() =>
              onSelectRange(index)
            }
          />
        ))}
      </div>

      <div className="actions">
        <Button
          variant="secondary"
          onClick={onAddTable}
          disabled={
            selectingTableIndex !== null
          }
        >
          + Add table
        </Button>

        <Button
          variant="primary"
          className="convert-button"
          onClick={onConvert}
          disabled={
            converting ||
            selectingTableIndex !== null
          }
        >
          {converting
            ? "Converting..."
            : "Convert to JSON"}
        </Button>
      </div>
    </section>
  );
}

export default TableList;
