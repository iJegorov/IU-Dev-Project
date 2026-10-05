import type {
  AnalyzeResponse,
  TableRange,
} from "../types/excel";

const API_BASE_URL = "http://127.0.0.1:9000";

export async function analyzeWorkbook(
  file: File
): Promise<AnalyzeResponse> {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(
    `${API_BASE_URL}/api/analyze`,
    {
      method: "POST",
      body: formData,
    }
  );

  if (!response.ok) {
    let message =
      "Failed to analyse the file.";

    try {
      const errorData = await response.json();

      if (errorData.detail) {
        message = errorData.detail;
      }
    } catch {
      // Keep the default error message.
    }

    throw new Error(message);
  }

  return response.json();
}

export async function convertWorkbook(
  file: File,
  tables: TableRange[]
): Promise<Blob> {
  const formData = new FormData();

  formData.append("file", file);

  formData.append(
    "ranges",
    JSON.stringify(tables)
  );

  const response = await fetch(
    `${API_BASE_URL}/api/convert`,
    {
      method: "POST",
      body: formData,
    }
  );

  if (!response.ok) {
    let message =
      "Failed to convert the file.";

    try {
      const errorData = await response.json();

      if (errorData.detail) {
        message = errorData.detail;
      }
    } catch {
      // Keep the default error message.
    }

    throw new Error(message);
  }

  return response.blob();
}