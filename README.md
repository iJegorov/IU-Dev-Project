XLSX to JSON Converter
 - A web application that detects tables in an Excel workbook and converts them into separate JSON files. Users can review and adjust detected table ranges before exporting the data.

Requirements
 - Git
 - Docker Desktop or Docker Engine with Docker Compose

How to Run
 1. Clone the repository:
    git clone YOUR_GITHUB_REPOSITORY_URL
    cd xlsx_to_json

 2. Build and start the application:
    docker compose up --build

 3. Open the application in your browser:
    - Frontend: http://localhost:5173
    - Backend API documentation: http://localhost:9000/docs
