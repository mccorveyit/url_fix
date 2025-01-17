import smartsheet
import os
import modules
import logging
from datetime import datetime

# set the API access token
API_TOKEN = os.getenv("Justin_API_Key")
TS = datetime.now().strftime('%Y-%m-%d-%H%M%S')
logging.basicConfig(
    # filename='url_fix'+TS+'.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[ 
        logging.FileHandler('Logs/url_fix_logs/'+TS+'.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# initialize client
ss = smartsheet.Smartsheet(API_TOKEN)
src_sheet_id = 6375545637916548
# get source sheet (URL_fix)
logger.info('Script started.')
src_sheet = ss.Sheets.get_sheet(src_sheet_id)

# get source sheet columns (URL_fix)
def main():
    src_columns = modules.get_src_sheet_columns(ss, src_sheet_id)
    print(f"URL_fix Columns: {src_columns}")

    responses = modules.update_rows(src_sheet_id)
    print(f"Response: {responses}")

    logger.info('Script executed successfully.')

if __name__ == "__main__":
    main()
    
