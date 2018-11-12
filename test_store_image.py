import os.path
import sqlite3

from store_image import database


def test_file_created(run_store_image):
    file_exist_bool = os.path.exists(run_store_image)
    assert file_exist_bool, f"Image {run_store_image} wasn\'t created"


def test_file_exist_in_db(run_store_image):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("SELECT * FROM images WHERE image_path=?", (run_store_image,))
    rows = cur.fetchall()
    number_of_rows = len(rows)
    if number_of_rows == 1:
        pass
    else:
        assert False, f"Found number of rows: {number_of_rows}, sql row: {rows}"