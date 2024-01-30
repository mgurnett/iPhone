#!/usr/bin/python
from datetime import datetime
import sqlite3
from sqlite3 import Error
import sys

def open_db (db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(f'{db_file}.db',
                               detect_types=sqlite3.PARSE_DECLTYPES |
                               sqlite3.PARSE_COLNAMES)
    except Error as e:
        print(e)
    return conn  

def close_db (conn):
    if conn:
        conn.close()
    
# create table in database
def create_db (conn, table_name):
    cur = conn.cursor()
    cur.execute(f"create table if not exists {table_name} (id INTEGER PRIMARY KEY, scale integer, note text, date_time integer);")

def write_data (db_name, table_name, scale, note, date_time):
    conn = open_db (db_name)
    cur = conn.cursor()
    cur.execute(f"INSERT INTO {table_name} (scale, note, date_time) VALUES (?, ?, ?)",
        (scale, note, date_time))
    conn.commit()
    cur.close()

def read_data (db_name, table_name):
    conn = open_db (db_name)
    cur = conn.cursor()
    sqlite_select_query = f"SELECT * from {table_name}"
    cur.execute(sqlite_select_query)
    records = cur.fetchall()
    cur.close()
    return records



if __name__ == '__main__':
    currentDateTime = datetime.now().timestamp()

    data_list = read_data ("Notions", "ideas")
    for data in data_list:
        time_stamp = datetime.fromtimestamp (data[3])
        print(f"Id: {data[0]} Scale: {data[1]} Note: {data[2]} at {time_stamp:%d-%m-%Y %-I:%M:%S}")

    write_data ("Notions", "ideas", 10, "over by the fence", currentDateTime)
    
    #proper end of python
    sys.exit(1)
