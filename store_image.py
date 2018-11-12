import os
import urllib
import re
import sqlite3
import datetime
import requests
from urllib.request import Request
from os.path import dirname, abspath, join

randomfox_url = 'https://randomfox.ca/floof/'
database = 'C:\\sqlite\\test_db.db'

sql_create_images_table = """ CREATE TABLE IF NOT EXISTS images (
                                    id integer PRIMARY KEY autoincrement,
                                    image_path text NOT NULL,
                                    created_date text,
                                    image_size integer
                                ); """

sql_insert_image = """ INSERT INTO images(image_path,created_date,image_size) VALUES(?,?,?) """

sql_find_by_image_path = """ SELECT * FROM images WHERE image_path=? """
sql_update_image = """ UPDATE images
                       SET image_path = ?,
                          created_date = ? ,
                          image_size = ?
                        WHERE image_path = ? """


def get_image_link(url) -> str:
    service_response = requests.get(url)
    service_json = service_response.json()
    image_link = service_json['image']
    return image_link


def download_image(image_link) -> str:
    image_name = re.search('(images/)(.*)', image_link).group(2)
    print("Image name: ", image_name)
    dir_path = join(abspath(dirname(__file__)), 'repository')
    image_path = join(dir_path, image_name)
    print("Image path: ", image_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    image_request = Request(image_link, headers={'User-Agent': 'Mozilla/5.0'})
    resource = urllib.request.urlopen(image_request)
    with open(image_path, 'wb') as f:
        f.write(resource.read())
    return image_path


def get_file_param(image_path) -> tuple:
    file_time = datetime.datetime.utcfromtimestamp((os.path.getmtime(image_path))).__str__()
    size_bytes = os.path.getsize(image_path)
    print("Size: ", size_bytes)
    print("Time: ", file_time)
    return (image_path,
            file_time,
            size_bytes)


def create_images_table(conn) -> None:
    try:
        with conn:
            conn.execute(sql_create_images_table)
    except sqlite3.Error as e:
        print(e)


def add_image(conn, param) -> None:
    try:
        with conn:
            conn.execute(sql_insert_image, param)
    except sqlite3.Error as e:
        print(e)


def check_one_image_exist(conn, image_path) -> bool:
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(sql_find_by_image_path, (image_path,))
            rows = cursor.fetchall()
            if len(rows) >= 1:
                return True
            else:
                return False
    except sqlite3.Error as e:
        print(e)


def update_image(conn, param) -> None:
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(sql_update_image, (*param, param[0]))
    except sqlite3.Error as e:
        print(e)


def save_image_to_db(file_param) -> None:
    conn = sqlite3.connect(database)
    create_images_table(conn)
    if check_one_image_exist(conn, file_param[0]):
        update_image(conn, file_param)
    else:
        add_image(conn, file_param)


def main() -> str:
    image_link = get_image_link(randomfox_url)
    image_path = download_image(image_link)
    file_param = get_file_param(image_path)
    save_image_to_db(file_param)
    return image_path


if __name__ == '__main__':
    main()
