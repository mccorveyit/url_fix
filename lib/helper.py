import os
import smartsheet
import pyodbc
import logging
import pdb

# define SQL table
sqltkn = os.getenv('sqlro_McData')
SQL_TABLE_NAME = "SS_sheets_path"

# set the API access token
API_TOKEN = os.getenv("Justin_API_Key")
logger = logging.getLogger(__name__)

# initialize client
ss = smartsheet.Smartsheet(API_TOKEN)
ss.errors_as_exceptions(True)
src_sheet_id = 6375545637916548
src_sheet = ss.Sheets.get_sheet(src_sheet_id)
# sheet_dict = {}

# define SQL connection string
def connect_to_sql():
    conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};Server=MSM-DYNSQLTEST\\mcdata;Database=MCDATA1;Trusted_Connection=yes;uid=sqlro;password=' + sqltkn)
    return conn

# retrieve the SQL table
def get_table_data():
    conn = connect_to_sql()
    query = f"SELECT * FROM {SQL_TABLE_NAME}"
    with conn.cursor() as cursor:
        cursor.execute(query)
        columns = [column[0]for column in cursor.description]
        rows = cursor.fetchall()
    conn.close()
    data = [dict(zip(columns, row)) for row in rows]
    return data

def get_permalink(sheet_id):
    try:
        conn = connect_to_sql()
        query = f"SELECT Permalink FROM {SQL_TABLE_NAME} WHERE ID = {sheet_id}"
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                logger.info(f"No permalink found for sheet ID {sheet_id}")
                return None
        conn.close()
    except pyodbc.Error as e:
        logger.error(f"Error retrieving permalink for sheet ID {sheet_id}: {e}")

# def main():
#     # get_table_data()
#     get_permalink(1000256545548164)
# def get_cell_by_name(row, column_name, tbl_colmn_map):
#     column_id = tbl_colmn_map.get(column_name)
#     if column_id is None:
#         return None
#     try:
#         c_value = row.get_column(column_id).display_value
#         if c_value is None:
#             c_value = row.get_column(column_id).value
#     except AttributeError:
#         c_value = row.get_column(column_id).value
#     except KeyError: 
#         return None
#     return c_value

# def get_workspace(workspace_id):
#     try:
#         workspace = ss.Workspaces.get_workspace(workspace_id)
#         return workspace
#     except smartsheet.exceptions.ApiError as e:
#         logger.error(f"Error retrieving workspace {workspace_id}: {e}")
#         return None
    
# def get_sheet_dict(workspace, sheet_dict):
#     try:
#         # Add sheets from the workspace
#         if len(workspace.sheets) > 0:
#             for sheet in workspace.sheets:
#                 sheet_dict[sheet.id] = sheet

#         # Add reports from the workspace
#         if len(workspace.reports) > 0:
#             for report in workspace.reports:
#                 sheet_dict[report.id] = report

#         # Recursively process folders
#         if len(workspace.folders) > 0:
#             for folder in workspace.folders:
#                 # Fetch the folder details to access its sheets and reports
#                 folder_details = ss.Folders.get_folder(folder.id)

#                 # Add sheets and reports from the folder
#                 if len(folder_details.sheets) > 0:
#                     for sheet in folder_details.sheets:
#                         sheet_dict[sheet.id] = sheet
#                 if len(folder_details.reports) > 0:
#                     for report in folder_details.reports:
#                         sheet_dict[report.id] = report

#                 # Recursively process subfolders
#                 get_sheet_dict(folder_details, sheet_dict)

#         return sheet_dict
#     except smartsheet.exceptions.ApiError as e:
#         logger.error(f"Error retrieving sheets from workspace {workspace.id}: {e}")

# def process_workspace(src_sheet, sheet_dict, columns):
#     try:
#         for src_row in src_sheet.rows:
#             perm_sheet_id_value = get_cell_by_name(src_row, "Id_source", columns)
#             target_column_value = get_cell_by_name(src_row, "url_target_column", columns)
#             sheet_id_value = get_cell_by_name(src_row, "Sheet ID", columns)
#             enable_value = get_cell_by_name(src_row, "Enable", columns)
#             src_row_id = src_row.id

#             if enable_value is not True:
#                 continue
#             # Get the sheet id sheet 
#             if sheet_id_value is None: 
#                 continue
#             sheet_id_sheet = ss.Sheets.get_sheet(sheet_id_value)
#             #Get workspace id from src_sheet
#             workspace_id = get_workspace(sheet_id_sheet._workspace.value)
#             if not workspace_id:
#                 logger.warning(f"Workspace ID not found for sheet {sheet_id_sheet.id_}")
#                 continue
#             workspace = get_workspace(workspace_id)
#             if not workspace:
#                 logger.warning(f"Workspace not found for sheet {sheet_id_sheet.id_}")
#                 continue
#             get_sheet_dict(workspace, sheet_dict)
#             # Check if the sheet ID is in the dictionary
#             # if sheet_id_value not in sheet_dict:
#             #     logger.warning(f"Sheet ID {sheet_id_value} not found in workspace")
#             #     continue
#             # # Get permalink for sheet 
#             # if sheet_id_value in sheet_dict:
#             #     permalink = sheet_dict[sheet_id_value].permalink
#             #     if hasattr(permalink, 'message') and permalink.message == '1006: Not Found':
#             #         logger.warning(f"Sheet or Report Not Found for ID {sheet_id_value}")
#             #         continue

#     except smartsheet.exceptions.ApiError as e:
#         logger.error(f"Error processing workspace for sheet {src_sheet.id}: {e}")
#         return None

# def process_permalink(perm_src_sheet, dest_sheet, dest_columns, dest_row, target_column_value, sheet_dict):
#     try:
#         #get the permalink from the sheet_dict 
#         perm_src_sheet_id = next((cell.display_value for cell in dest_row.cells if cell.column_id == dest_columns[perm_sheet_id_value]), None)
#         if perm_src_sheet_id is None:
#             logger.warning(f"Permalink Source Sheet ID not found for row {dest_row.id}")
#             return
#         # Check if the permalink exists in the sheet_dict
#         if perm_src_sheet_id not in sheet_dict:
#             logger.warning(f"Permalink Source Sheet ID {perm_src_sheet_id} not found in sheet_dict")
#             return
#         # Get the permalink from the sheet_dict
#         permalink = sheet_dict[perm_src_sheet_id].permalink
#         if hasattr(permalink, 'message') and permalink.message == '1006: Not Found':
#             logger.warning(f"Sheet or Report Not Found for ID {perm_src_sheet_id}")
#             return


# def main():
#     workspace_id = src_sheet.workspace.id_
#     workspace = get_workspace(workspace_id)
#     sheet_dict = {}  # Initialize sheet_dict locally
#     sheet_dict = get_sheet_dict(workspace, sheet_dict)
#     workingspace = process_workspace(src_sheet, sheet_dict, columns)
    # pdb.set_trace()
    # workspace_sheets = workspace._folders.sheets
    # return workspace
    # [(folder.id_, folder.name) for folder in workspace.folders] = ss.Folders.list_folders(workspace_id)
    # [(sheet.id_, sheet.name) for sheet in workspace._sheets] = ss.Sheets.list_sheets(workspace_id)
    # [(report.id_, report.name) for report in workspace._reports] = ss.Reports.list_reports(workspace_id)
    # [(sheet.id_, sheet) for sheet in workspace.folders]  = ss.Sheets.list_sheets(workspace_id)
    

# if __name__ == "__main__":
#     main()