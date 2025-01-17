# Destination sheet(dest_sheet): The Sheet ID Column
# Source Sheet(src_sheet): URL_fix
# Permalink Source Sheet(perm_src_sheet): Destination Sheet[Id_source] Column value where retrieve permalink

import smartsheet
import os
import pdb
import logging



# set the API access token
API_TOKEN = os.getenv("Justin_API_Key")
logger = logging.getLogger(__name__)

# initialize client
ss = smartsheet.Smartsheet(API_TOKEN)
ss.errors_as_exceptions(True)
src_sheet_id = 6375545637916548
src_sheet = ss.Sheets.get_sheet(src_sheet_id)
statuses = []
responses = []
permalinks = []

def get_src_sheet_columns(ss, sheet_id):
    sheet = ss.Sheets.get_sheet(sheet_id)
    column_info = {str(column.title): column.id for column in sheet.columns}
    return column_info

def get_dest_sheet_columns(ss, sheet_id):
    sheet = ss.Sheets.get_sheet(sheet_id)
    column_info = {str(column.title): column.id for column in sheet.columns}
    return column_info

def get_permalink(entity, default):
    if entity and hasattr(entity, "permalink"):
        return entity.permalink
    return default

def get_cell_by_name(row, column_name, tbl_colmn_map):
    column_id = tbl_colmn_map.get(column_name)
    if column_id is None:
        return None
    try:
        c_value = row.get_column(column_id).display_value
        if c_value is None:
            c_value = row.get_column(column_id).value
    except AttributeError:
        c_value = row.get_column(column_id).value
    except KeyError: 
        return None
    return c_value
    

def get_sheet_or_report(sheet_id):
    try:
        sheet = ss.Sheets.get_sheet(sheet_id)
    except:
        try:
            sheet = ss.Reports.get_report(sheet_id)
        except Exception as e:
            logger.error(f"GET_SHEET_OR_REPORT NONE Error: {e}")
            return None
    return sheet

def update_row(dest_sheet,row_values,dest_sheet_map,row_id):
    row = ss.models.Row()
    row.id = row_id
    for c_name in row_values:
        cell = ss.models.Cell()
        cell.column_id = dest_sheet_map[c_name]
        cell.value = row_values[c_name]
        cell.strict = False
        row.cells.append(cell)
    response = ss.Sheets.update_rows(dest_sheet.id, [row])
    return response

def process_permalink(perm_src_sheet, dest_sheet, dest_columns, dest_row, target_column_value, permalinks, responses, statuses):
    try:
        if hasattr(perm_src_sheet, 'error'):
            permalink = get_permalink(perm_src_sheet, "Error Processing")
            status = "Error Processing"
            statuses.append(status)
            update_row(dest_sheet=dest_sheet, row_values={target_column_value: ""}, dest_sheet_map=dest_columns, row_id=dest_row.id)
        elif hasattr(perm_src_sheet, "permalink"):
            permalink = perm_src_sheet.permalink
            status = "Done"
            if permalink != get_cell_by_name(dest_row, target_column_value, dest_columns):
                update_permalinks(dest_sheet=dest_sheet, dest_columns=dest_columns, permalinks=permalinks, responses=responses, permalink=permalink, dest_row=dest_row, target_column_value=target_column_value)
            statuses.append(status)
        else:
            permalink = "Permalink Not Found"
            status = "Error Processing"
            statuses.append(status)
            update_row(dest_sheet=dest_sheet, row_values={target_column_value: ""}, dest_sheet_map=dest_columns, row_id=dest_row.id)
            print(f"Error processing row {dest_row.rowNumber}")
    except:
        pass
    
def update_permalinks(dest_sheet, dest_columns, permalinks, responses, permalink, dest_row, target_column_value):
    try:    
        permalink_row = ss.models.Row()
        permalink_row.id = dest_row.id
        cell = ss.models.Cell()
        cell.column_id = dest_columns[target_column_value]
        cell.value = permalink
        cell.strict = False
        permalink_row.cells.append(cell)
        permalinks.append(permalink_row)

        if len(permalinks) >= 200:
            response = ss.Sheets.update_rows(dest_sheet.id, permalinks)
            responses.append(response)
            permalinks.clear()
            logger.info("Updated 200 permalinks")
    except Exception as e:
        logger.error(f"UPDATE_PERMALINKS Error: {e}")
        pass

def update_status(row_id, status, columns):
    row_values = {"Status": status}
    update_row(dest_sheet=src_sheet, row_values=row_values, dest_sheet_map=columns, row_id=row_id)

def process_src_sheet(src_sheet, columns, statuses, responses, permalinks):
    for src_row in src_sheet.rows:
        perm_sheet_id_value = get_cell_by_name(src_row, "Id_source", columns)
        target_column_value = get_cell_by_name(src_row, "url_target_column", columns)
        sheet_id_value = get_cell_by_name(src_row, "Sheet ID", columns)
        request_value = get_cell_by_name(src_row, "Request", columns)
        src_row_id = src_row.id

        if request_value is not True:
            continue

        # Get the destination sheet ID and fetch the destination sheet or error
        dest_sheet_id = sheet_id_value
        try:
            dest_sheet = get_sheet_or_report(dest_sheet_id)
            if not dest_sheet or hasattr(dest_sheet, 'message') and dest_sheet.message == '1006: Not Found':
                update_status(src_row_id, "Sheet or Report Not Found", columns)
                continue

            dest_columns = get_dest_sheet_columns(ss, dest_sheet_id)
            print(f"Destination Sheet Columns: {dest_columns}")

            if perm_sheet_id_value not in dest_columns:
                update_status(src_row_id, "Wrong Id_source", columns)
                update_row(dest_sheet=src_sheet, row_values={"Id_source": ""}, dest_sheet_map=columns, row_id=src_row_id)
                continue

            elif target_column_value not in dest_columns:
                update_status(src_row_id, "Wrong url_target_column", columns)
                update_row(dest_sheet=src_sheet, row_values={"url_target_column": ""}, dest_sheet_map=columns, row_id=src_row_id)
                continue
            process_dest_rows(dest_sheet, dest_columns, perm_sheet_id_value, target_column_value, statuses, responses, permalinks, src_row_id)
        except:
            continue
        all_done = all(status == "Done" for status in statuses)
        if all_done:
            status = "Done"
        else:
            status = "Error Processing"
        update_status(src_row_id, status, columns)

        # Update the status and permalinks if any
        if permalinks:
            response = ss.Sheets.update_rows(dest_sheet.id, permalinks)
            responses.append(response)
            permalinks.clear()
            update_status(src_row_id, status, columns)
        statuses = []

def process_dest_rows(dest_sheet, dest_columns, perm_sheet_id_value, target_column_value, statuses, responses, permalinks, src_row_id):
    for dest_row in dest_sheet.rows: 
            try:
                perm_src_sheet_id = next((cell.display_value for cell in dest_row.cells if cell.column_id == dest_columns[perm_sheet_id_value]), None)
                print(f"Permalink Source Sheet ID: {perm_src_sheet_id}")
                if perm_src_sheet_id == None:
                    continue

                # dest_row_id = dest_row.id
                perm_src_sheet = get_sheet_or_report(perm_src_sheet_id)
                process_permalink(perm_src_sheet, dest_sheet, dest_columns, dest_row, target_column_value, permalinks, responses, statuses)
            except KeyError:
                continue

            except:
                continue
            
def update_rows(sheet_id):
    columns = get_src_sheet_columns(ss, sheet_id)
    statuses = []
    responses = []
    permalinks = []
    src_row_id = None
    dest_sheet = None
    row_id = None

    process_src_sheet(src_sheet, columns, statuses, responses, permalinks)

    return responses

