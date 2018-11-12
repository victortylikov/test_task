import os.path
import re
import sqlite3
import datetime
from store_image import database


def test_file_created(run_store_image):
    file_exist_bool = os.path.exists(run_store_image)
    assert file_exist_bool, f"Image {run_store_image} wasn\'t created"


def test_file_size_greater_than_zero(run_store_image):
    size_bytes = os.path.getsize(run_store_image)
    assert size_bytes > 0, f"File size {size_bytes}"


def test_file_exist_in_db(run_store_image):
    rows = _get_image_row_from_db(run_store_image)
    number_of_rows = len(rows)
    if number_of_rows == 1:
        pass
    else:
        assert False, f"Found number of rows: {number_of_rows}, sql row: {rows}"


def test_image_size_and_date(run_store_image):
    db_rows = _get_image_row_from_db(run_store_image)
    file_time = datetime.datetime.utcfromtimestamp((os.path.getmtime(run_store_image))).__str__()
    size_bytes = os.path.getsize(run_store_image)
    real_data = (run_store_image, file_time, size_bytes)
    first_row = db_rows[0]
    assert first_row[1:] == real_data, \
        f"DB data: {first_row[1:]} doesn't match with real data: {real_data}"


# Don't use this test with large data 
def test_number_of_files_match_number_of_db_rows(run_store_image):
    dir_path = re.sub("([0-9]*.jpg$)", "", run_store_image)
    number_files_in_folder = len(os.listdir(dir_path))
    number_rows_in_db = _get_row_number()
    assert number_files_in_folder == number_rows_in_db,\
        F"Real number of files in folder: {number_files_in_folder}, number rows in db {number_rows_in_db}"


def _get_image_row_from_db(run_store_image) ->list:
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("SELECT * FROM images WHERE image_path=?", (run_store_image,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def _get_row_number() -> int:
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM images")
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row[0]
