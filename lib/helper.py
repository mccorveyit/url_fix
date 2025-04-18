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
def get_sheet_dict(sheet_ids):
    try:
        conn = connect_to_sql()
        sheet_ids_str = ', '.join(f"'{sheet_id}'" for sheet_id in sheet_ids)
        query = f"SELECT ID, Permalink FROM {SQL_TABLE_NAME} WHERE ID IN ({sheet_ids_str})"
        # query = f"SELECT Permalink FROM {SQL_TABLE_NAME} WHERE ID IN ({','.join(map(str, sheet_ids))})"

        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        conn.close()

        permalink_dict = {row[0]: row[1] for row in results}
        return permalink_dict
    except pyodbc.Error as e:
        logger.error(f"Error retrieving data from SQL table: {e}")
        return None

# def get_permalink(sheet_id):
#     try:
#         conn = connect_to_sql()
#         query = f"SELECT Permalink FROM {SQL_TABLE_NAME} WHERE ID = {sheet_id}"
#         with conn.cursor() as cursor:
#             cursor.execute(query)
#             result = cursor.fetchone()
#             if result:
#                 return result[0]
#             else:
#                 logger.info(f"No permalink found for sheet ID {sheet_id}")
#                 return None
#         conn.close()
#     except pyodbc.Error as e:
#         logger.error(f"Error retrieving permalink for sheet ID {sheet_id}: {e}")
#         return None