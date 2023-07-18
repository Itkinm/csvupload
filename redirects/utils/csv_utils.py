import pygsheets
import os
import pandas as pd

from redirects.utils.auth_utils import create_credentials


def upload_csv(file_name, tg_id):

    credentials = create_credentials(tg_id)

    gc = pygsheets.authorize(custom_credentials = credentials)

    content = pd.read_csv(file_name)
    os.remove(file_name)

    sh = gc.create(file_name)
    wh = sh.worksheet_by_title('Sheet1')
    wh.set_dataframe(content, "A1", copy_index=False, copy_head=True, extend=True, fit=False, escape_formulae=True)

    return sh
