import pytest
from unittest.mock import MagicMock, patch
import smartsheet
import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from lib.modules import *
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CustomMagicMock(MagicMock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = []
    def add_data(self, value):
        self._data.append(value)
    def get_data(self):
        return self._data

# Test case for get_dest_sheet_columns
@pytest.fixture
def mock_smartsheet_client():
    mock_client = CustomMagicMock()
    # breakpoint()
    return mock_client

def pytest_assertrepr_compare(op, left, right):
    if isinstance(left, CustomMagicMock) and isinstance(right, CustomMagicMock) and op == "==":
        if left.get_data() != right.get_data():
            logger.error(f"Assertion failed: {left.get_data()} != {right.get_data()}")
        return ["Assertion failed:", f"{left.get_data()} != {right.get_data()}"]

def test_custom_mock(mock_smartsheet_client):
    # Call the additional method on the custom mock
    mock_smartsheet_client.add_data("Value 1")
    mock_smartsheet_client.add_data("Value 2")
    # Get the data from the custom mock
    data = mock_smartsheet_client.get_data()
    # Assert the data retrieved from the custom mock
    assert data == ["Value 1", "Value 2"]
    print(f"Data: {data}")


def test_get_src_sheet_columns(mock_smartsheet_client):
    # Arrange: Mock the response from the Smartsheet API for the given sheet ID
    mock_column_1 = MagicMock()
    mock_column_1.title = "Sheet ID"
    mock_column_1.id = 6251968876203908

    mock_column_2 = MagicMock()
    mock_column_2.title = "Id_source"
    mock_column_2.id = 4000169062518660

    mock_column_3 = MagicMock()
    mock_column_3.title = "url_target_column"
    mock_column_3.id = 8503768689889156

    mock_column_4 = MagicMock()
    mock_column_4.title = "Status"
    mock_column_4.id = 340994365280132

    # Mock the sheet's columns list
    mock_columns = [mock_column_1, mock_column_2, mock_column_3, mock_column_4]

    mock_sheet = MagicMock()
    mock_sheet.columns = mock_columns

    mock_smartsheet_client.Sheets.get_sheet.return_value = mock_sheet

    # Act: Call the function you're testing, using the mock client
    result = get_src_sheet_columns(mock_smartsheet_client, 6375545637916548)

    # Assert: Verify the result
    expected_result = {
        "Sheet ID": 6251968876203908,
        "Id_source": 4000169062518660,
        "url_target_column": 8503768689889156,
        "Status": 340994365280132
    }
    assert result == expected_result

    # Verify that get_sheet was called once with the correct sheet ID
    mock_smartsheet_client.Sheets.get_sheet.assert_called_once_with(6375545637916548)

def test_get_dest_sheet_columns(mock_smartsheet_client):
    # Arrange: Mock the response from the Smartsheet API for the given sheet ID
    mock_column_1 = MagicMock()
    mock_column_1.title = "Primary Column"
    mock_column_1.id = 5828169588494212

    mock_column_2 = MagicMock()
    mock_column_2.title = "ROWID"
    mock_column_2.id = 3576369774808964

    mock_column_3 = MagicMock()
    mock_column_3.title = "Rowcount"
    mock_column_3.id = 8079969402179460

    mock_column_4 = MagicMock()
    mock_column_4.title = "In Id"
    mock_column_4.id = 761620007702404

    mock_column_5 = MagicMock()
    mock_column_5.title = "In Link"
    mock_column_5.id = 5265219635072900

    mock_column_6 = MagicMock()
    mock_column_6.title = "In Id is Report"
    mock_column_6.id = 3013419821387652

    mock_column_7 = MagicMock()
    mock_column_7.title = "In Column"
    mock_column_7.id = 7517019448758148

    mock_column_8 = MagicMock()
    mock_column_8.title = "Out Sheet Id"
    mock_column_8.id = 1887519914545028

    mock_column_9 = MagicMock()
    mock_column_9.title = "Out Link"
    mock_column_9.id = 6391119541915524

    mock_column_10 = MagicMock()
    mock_column_10.title = "Out Column"
    mock_column_10.id = 4139319728230276

    mock_column_11 = MagicMock()
    mock_column_11.title = "Notes"
    mock_column_11.id = 8642919355600772

    mock_column_12 = MagicMock()
    mock_column_12.title = "Sorted"
    mock_column_12.id = 480145030991748

    mock_column_13 = MagicMock()
    mock_column_13.title = "Primary Contact"
    mock_column_13.id = 4983744658362244

    mock_column_14 = MagicMock()
    mock_column_14.title = "Active"
    mock_column_14.id = 2731944844676996

    mock_column_15 = MagicMock()
    mock_column_15.title = "Error Description"
    mock_column_15.id = 7235544472047492

    mock_column_16 = MagicMock()
    mock_column_16.title = "Last Script Update"
    mock_column_16.id = 1606044937834372


    # Mock the sheet's columns list
    mock_columns = [
        mock_column_1, mock_column_2, 
        mock_column_3, mock_column_4, 
        mock_column_5, mock_column_6, 
        mock_column_7, mock_column_8, 
        mock_column_9, mock_column_10, 
        mock_column_11, mock_column_12, 
        mock_column_13, mock_column_14, 
        mock_column_15, mock_column_16
    ]

    mock_sheet = MagicMock()
    mock_sheet.columns = mock_columns

    mock_smartsheet_client.Sheets.get_sheet.return_value = mock_sheet
    # Act: Call the function you're testing, using the mock client
    result = get_dest_sheet_columns(mock_smartsheet_client, 3698191069302660)

    # Assert: Verify the result
    expected_result = {
        "Primary Column": 5828169588494212,
        "ROWID": 3576369774808964,
        "Rowcount": 8079969402179460,
        "In Id": 761620007702404,
        "In Link": 5265219635072900,
        "In Id is Report": 3013419821387652,
        "In Column": 7517019448758148,
        "Out Sheet Id": 1887519914545028,
        "Out Link": 6391119541915524,
        "Out Column": 4139319728230276,
        "Notes": 8642919355600772,
        "Sorted": 480145030991748,
        "Primary Contact": 4983744658362244,
        "Active": 2731944844676996,
        "Error Description": 7235544472047492,
        "Last Script Update": 1606044937834372
    }
    assert result == expected_result

    # Verify that get_sheet was called once with the correct sheet ID
    mock_smartsheet_client.Sheets.get_sheet.assert_called_once_with(3698191069302660)

def test_get_permalink():
    # Test case where entity has a permalink attribute
    mock_entity_with_permalink = MagicMock()
    mock_entity_with_permalink.permalink = "http://example.com/permalink"
    assert get_permalink(mock_entity_with_permalink, "default") == "http://example.com/permalink"

    # Test case where entity does not have a permalink attribute
    mock_entity_without_permalink = MagicMock()
    del mock_entity_without_permalink.permalink
    assert get_permalink(mock_entity_without_permalink, "default") == "default"

    # Test case where entity is None
    assert get_permalink(None, "default") == "default"

def test_get_cell_by_name():
    # Arrange: Mock the row and column map
    mock_row = MagicMock()
    mock_column_map = {
        "Column1": 123,
        "Column2": 456
    }

    # Mock the cell with display_value
    mock_cell_with_display_value = MagicMock()
    mock_cell_with_display_value.display_value = "Display Value"
    mock_row.get_column.return_value = mock_cell_with_display_value

    # Act: Call the function with a column that has display_value
    result = get_cell_by_name(mock_row, "Column1", mock_column_map)
    assert result == "Display Value"

    # Mock the cell without display_value but with value
    mock_cell_with_value = MagicMock()
    del mock_cell_with_value.display_value
    mock_cell_with_value.value = "Value"
    mock_row.get_column.return_value = mock_cell_with_value

    # Act: Call the function with a column that has value
    result = get_cell_by_name(mock_row, "Column2", mock_column_map)
    assert result == "Value"

    # Mock the cell not found scenario
    mock_row.get_column.side_effect = KeyError("Column3")
    result = get_cell_by_name(mock_row, "Column3", mock_column_map)
    assert result is None

# @patch('url_fix.lib.modules.ss.Sheets.get_sheet')
# @patch('url_fix.lib.modules.ss.Reports.get_report')
# def test_get_sheet_or_report():#mock_get_report, mock_get_sheet):
#     with patch('url_fix.lib.modules.ss.Sheets.get_sheet') as mock_get_sheet, \
#         patch('url_fix.lib.modules.ss.Reports.get_report') as mock_get_report:

#         # Test case where the sheet is successfully retrieved
#         mock_sheet = MagicMock()
#         mock_sheet.id = 12345
#         mock_get_sheet.return_value = mock_sheet
#         result = get_sheet_or_report(mock_sheet.id)
#         breakpoint()
#         print(result)
#         assert result == mock_sheet  # Ensure the mock sheet is returned
#         mock_get_sheet.assert_called_once_with(12345)
#         mock_get_sheet.reset_mock()
        
#         # Test case where the sheet is not found but the report is retrieved
#         mock_get_sheet.side_effect = smartsheet.exceptions.ApiError({
#             'errorCode': 1006,
#             'message': "Not Found",
#             'refId': "ref_id",
#             'statusCode': 404
#         })
#         mock_report = MagicMock()
#         mock_get_report.return_value = mock_report
#         result = get_sheet_or_report(12345)
#         assert result == mock_report  # Ensure the report is returned in case of sheet not found
#         mock_get_report.assert_called_once_with(12345)
#         mock_get_sheet.reset_mock()
#         mock_get_report.reset_mock()
        
#         # Test case where neither the sheet nor the report is found
#         mock_get_sheet.side_effect = smartsheet.exceptions.ApiError({
#             'errorCode': 1006,
#             'message': "Not Found",
#             'refId': "ref_id",
#             'statusCode': 404
#         })
#         mock_get_report.side_effect = smartsheet.exceptions.ApiError({
#             'errorCode': 1006,
#             'message': "Not Found",
#             'refId': "ref_id",
#             'statusCode': 404
#         })
#         result = get_sheet_or_report(12345)
#         assert result is None  # Ensure None is returned if both sheet and report fail
#         mock_get_sheet.assert_called_once_with(12345)
#         mock_get_report.assert_called_once_with(12345)

@patch("smartsheet.Sheets")
def test_update_row(mock_sheets):
    # Arrange
    mock_dest_sheet = MagicMock()
    mock_dest_sheet.id = 12345

    mock_row_values = {
        "Column1": "Value1",
        "Column2": "Value2"
    }

    mock_dest_sheet_map = {
        "Column1": 1111,
        "Column2": 2222
    }

    mock_row_id = 67890

    # Mock the response of the Smartsheet update_rows call
    mock_response = MagicMock()
    mock_sheets.update_rows.return_value = mock_response

    # Act
    with patch("smartsheet.models.Row") as MockRow, patch("smartsheet.models.Cell") as MockCell:
        mock_row = MockRow()
        mock_cell_1 = MockCell()
        mock_cell_1.column_id = mock_dest_sheet_map["Column1"]
        mock_cell_1.value = "Value1"
        mock_cell_1.strict = False

        mock_cell_2 = MockCell()
        mock_cell_2.column_id = mock_dest_sheet_map["Column2"]
        mock_cell_2.value = "Value2"
        mock_cell_2.strict = False

        mock_row.cells = [mock_cell_1, mock_cell_2]
        MockRow.return_value = mock_row
        MockCell.side_effect = [mock_cell_1, mock_cell_2]

        response = update_row(mock_dest_sheet, mock_row_values, mock_dest_sheet_map, mock_row_id)

    # Assert
    assert response == mock_response
    mock_sheets.update_rows.assert_called_once_with(mock_dest_sheet.id, [mock_row])
    assert mock_row.id == mock_row_id
    assert len(mock_row.cells) == len(mock_row_values)

    # Check if the cells were created correctly
    for i, (c_name, value) in enumerate(mock_row_values.items()):
        assert mock_row.cells[i].column_id == mock_dest_sheet_map[c_name]
        assert mock_row.cells[i].value == value
        assert mock_row.cells[i].strict is False
