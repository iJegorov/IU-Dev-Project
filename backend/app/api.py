
import json
import re
import shutil
import tempfile
import zipfile
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.models.api_models import (
    AnalyzeResponse,
    TableRangeResponse,
)
from app.models.table_range import (
    TableRange,
    parse_excel_range,
)
from app.xlsx_to_json import (
    analyze_excel,
    convert_excel_to_json,
)


app = FastAPI(
    title="XLSX to JSON Converter API",
    description="API for analysing Excel files and converting tables to JSON.",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "XLSX to JSON Converter API",
        "status": "running",
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
    }


@app.post(
    "/api/analyze",
    response_model=AnalyzeResponse,
)
async def analyze(
    file: UploadFile = File(...),
):
    """
    Upload an XLSX file and automatically detect table ranges.
    """

    validate_excel_file(file)

    with tempfile.TemporaryDirectory() as temp_directory:
        input_path = (
            Path(temp_directory)
            / safe_filename(file.filename)
        )

        await save_uploaded_file(
            file,
            input_path,
        )

        try:
            detected_ranges = analyze_excel(
                input_path
            )

        except Exception as exc:
            raise HTTPException(
                status_code=400,
                detail=f"Could not analyse Excel file: {exc}",
            ) from exc

    tables = [
        TableRangeResponse(
            name=table_range.name,
            range=table_range.range_string,
            start_row=table_range.start_row,
            start_column=table_range.start_column,
            end_row=table_range.end_row,
            end_column=table_range.end_column,
        )
        for table_range in detected_ranges
    ]

    return AnalyzeResponse(
        filename=file.filename or "uploaded.xlsx",
        tables=tables,
    )


@app.post("/api/convert")
async def convert(
    file: UploadFile = File(...),
    ranges: str | None = Form(None),
):
    """
    Upload an XLSX file and convert selected table ranges to JSON.

    If ranges is omitted, automatic table detection is used.

    If ranges is provided, automatic detection is completely overridden.
    """

    validate_excel_file(file)

    user_ranges = parse_user_ranges(ranges)

    temp_directory = Path(
        tempfile.mkdtemp()
    )

    input_path = (
        temp_directory
        / safe_filename(file.filename)
    )

    output_directory = (
        temp_directory
        / "output"
    )

    try:
        await save_uploaded_file(
            file,
            input_path,
        )

        generated_files = convert_excel_to_json(
            input_path,
            output_directory,
            user_ranges=user_ranges,
        )

        if not generated_files:
            shutil.rmtree(
                temp_directory,
                ignore_errors=True,
            )

            raise HTTPException(
                status_code=400,
                detail="No tables containing data were found.",
            )

        zip_path = (
            temp_directory
            / "converted_json.zip"
        )

        create_zip_file(
            generated_files,
            zip_path,
        )

        from starlette.background import BackgroundTask

        cleanup_task = BackgroundTask(
            shutil.rmtree,
            temp_directory,
            ignore_errors=True,
        )

        return FileResponse(
            path=zip_path,
            media_type="application/zip",
            filename="converted_json.zip",
            background=cleanup_task,
        )

    except HTTPException:
        raise

    except Exception as exc:
        shutil.rmtree(
            temp_directory,
            ignore_errors=True,
        )

        raise HTTPException(
            status_code=400,
            detail=f"Could not convert Excel file: {exc}",
        ) from exc


def validate_excel_file(
    file: UploadFile,
):
    """Validate the uploaded file type."""

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename was provided.",
        )

    extension = Path(
        file.filename
    ).suffix.lower()

    if extension not in {".xlsx", ".xlsm"}:
        raise HTTPException(
            status_code=400,
            detail="Only XLSX and XLSM files are supported.",
        )


def safe_filename(
    filename: str | None,
) -> str:
    """
    Prevent path traversal and keep only a safe filename.
    """

    if not filename:
        return "uploaded.xlsx"

    filename = Path(filename).name

    filename = re.sub(
        r"[^A-Za-z0-9._-]",
        "_",
        filename,
    )

    return filename


async def save_uploaded_file(
    file: UploadFile,
    destination: Path,
):
    """Save an uploaded file to disk."""

    with open(
        destination,
        "wb",
    ) as output_file:
        while chunk := await file.read(1024 * 1024):
            output_file.write(chunk)


def parse_user_ranges(
    ranges_json: str | None,
) -> list[TableRange] | None:
    """
    Parse user-defined ranges received from the frontend.

    Expected format:

    [
        {
            "name": "products",
            "range": "A1:C5"
        }
    ]

    None means automatic detection should be used.
    """

    if ranges_json is None or not ranges_json.strip():
        return None

    try:
        ranges_data = json.loads(
            ranges_json
        )

    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=400,
            detail="Invalid ranges JSON.",
        ) from exc

    if not isinstance(ranges_data, list):
        raise HTTPException(
            status_code=400,
            detail="Ranges must be a JSON array.",
        )

    table_ranges = []

    for index, item in enumerate(ranges_data):

        if not isinstance(item, dict):
            raise HTTPException(
                status_code=400,
                detail=f"Range {index + 1} must be an object.",
            )

        name = item.get("name")
        range_string = item.get("range")

        if not name:
            raise HTTPException(
                status_code=400,
                detail=f"Range {index + 1} is missing a name.",
            )

        if not range_string:
            raise HTTPException(
                status_code=400,
                detail=f"Range {index + 1} is missing a range.",
            )

        try:
            table_range = parse_excel_range(
                range_string,
                name=name,
            )

        except ValueError as exc:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Invalid range '{range_string}': {exc}"
                ),
            ) from exc

        table_ranges.append(
            table_range
        )

    return table_ranges


def create_zip_file(
    files: list[Path],
    zip_path: Path,
):
    """Create a ZIP archive containing generated JSON files."""

    with zipfile.ZipFile(
        zip_path,
        "w",
        compression=zipfile.ZIP_DEFLATED,
    ) as archive:

        for file_path in files:
            archive.write(
                file_path,
                arcname=file_path.name,
            )
