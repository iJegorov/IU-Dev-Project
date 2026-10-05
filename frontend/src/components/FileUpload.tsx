
import { useRef } from "react";
import Button from "./Button";

interface FileUploadProps {
  file: File | null;
  loading: boolean;
  onFileSelected: (file: File) => void | Promise<void>;
}

function FileUpload({
  file,
  loading,
  onFileSelected,
}: FileUploadProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  function handleFileChange(
    event: React.ChangeEvent<HTMLInputElement>
  ) {
    const selectedFile = event.target.files?.[0];

    if (selectedFile) {
      onFileSelected(selectedFile);
    }
  }

  function handleDrop(
    event: React.DragEvent<HTMLDivElement>
  ) {
    event.preventDefault();

    const droppedFile = event.dataTransfer.files?.[0];

    if (droppedFile) {
      onFileSelected(droppedFile);
    }
  }

  function handleDragOver(
    event: React.DragEvent<HTMLDivElement>
  ) {
    event.preventDefault();
  }

  return (
    <section className="upload-card">
      <div
        className="drop-zone"
        onDrop={handleDrop}
        onDragOver={handleDragOver}
      >
        <p className="eyebrow">
          Excel workbook
        </p>

        <h2>
          Upload your workbook
        </h2>

        <p>
          Drag and drop an XLSX or XLSM file here,
          or choose one from your computer.
        </p>

        <input
          ref={inputRef}
          type="file"
          accept=".xlsx,.xlsm"
          onChange={handleFileChange}
          hidden
        />

        <Button
          type="button"
          onClick={() => inputRef.current?.click()}
          disabled={loading}
        >
          Choose file
        </Button>

        {file && (
          <p className="selected-file">
            Selected: <strong>{file.name}</strong>
          </p>
        )}

        {loading && (
          <p className="upload-status">
            Analyzing workbook...
          </p>
        )}
      </div>
    </section>
  );
}

export default FileUpload;

