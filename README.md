# Smartsheet URL Fix Script

This script automates the processing and updating of permalinks in Smartsheet. It uses the Smartsheet API to fetch data, update rows, and manage permalinks efficiently. 

## Features
- Aquires permalinks from a list of sheets or reports and writes it to specified column.
- Fetches columns and rows from Smartsheet sheets or reports.
- Processes and updates row data based on specific logic.
- Supports bulk updates for improved performance.
- Handles errors and logs them for easier debugging.

## Prerequisites
1. **Python 3.7+**
2. **Smartsheet SDK for Python**:
   Install the SDK using pip:
   ```bash
   pip install smartsheet-python-sdk
3. **API Token:** Obtain your Smartsheet API token and set it as an environment variable:
    ```bash
    export Justin_API_Key=<your_api_token>
4. **Smartsheet Access:** Ensure you have the necessary permissions to access and modify the sheets.:

## Setup
1. Clone or download this repository.

2. Set your API Token in the environment
    ```bash
    export Justin_API_Key=<your_api_token>

## Usage
The script includes several functions for interacting with Smartsheet. Below are the key functions and their usage:

1. `get_src_sheet_columns(ss, sheet_id)`

    Fetches column metadata for a source sheet.

    **Parameters:**

    `ss`: Smartsheet client object.
    `sheet_id`: ID of the source sheet.

    **Returns:**

    Dictionary mapping column titles to column IDs.

2. `update_row(dest_sheet, row_values, dest_sheet_map, row_id)`

    Updates a specific row in the destination sheet.

    **Parameters:**

    `dest_sheet`: Destination Smartsheet object.
    `row_values`: Dictionary of column names and values to update.
    `dest_sheet_map`: Mapping of destination column names to IDs.
    `row_id`: ID of the row to update.

    **Returns:**

    Response from the Smartsheet API.

3. `process_src_sheet(src_sheet, columns, statuses, responses, permalinks)`

    Processes rows from the source sheet and updates the destination sheet.

    **Parameters:**

    `src_sheet`: Source sheet object.
    `columns`: Column mapping for the source sheet.
    `statuses`: List to store row statuses.
    `responses`: List to store API responses.
    `permalinks`: List of permalink rows to update.

4. `update_rows(sheet_id)`

    Entry point for the script. Processes the source sheet rows and updates destination sheets.

    **Parameters:**

    `sheet_id`: ID of the source sheet.

    **Returns:**

    List of API responses.

## Example Execution
To update rows for a given source sheet, call the `update_rows` function with the sheet ID:
```bash
update_rows(123123123123)
```

## Error Handeling
- The script uses try-except blocks to handle API and processing errors.
- Errors are logged using Python's logging module.

## Logging
Logs are generated to provide information about processing, errors, and status updates. Customize the logging configuration as needed. Logs are stored in the Logs directory format (Year-month-day-hourrminutsecond)

## Statuses
- **Done** - Sheet completed and updated the list of sheets/reports with the correct permalinks
- **Error Processing** - There were one or more sheets/reports in the list that could not be found. (permalink will be blank)
- **Wrong Id_source** - The column name in the `Id_source` column was not found on the destination sheet 
- **Wrong url_target_column** - The column name in the `url_target_column` was not found on the destination sheet
- **Sheet or Report Not Found** - The Sheet ID in the `Sheet ID` column was not found.
