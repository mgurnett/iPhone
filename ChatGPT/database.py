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
def create_db (db_name, table_name):
    conn = open_db (db_name)
    cur = conn.cursor()
    cur.execute(f"create table if not exists {table_name} (id INTEGER PRIMARY KEY, scale integer, note text, date_time integer);")

def write_data (db_name, table_name, scale, note, date_time):
    conn = open_db (db_name)
    cur = conn.cursor()
    cur.execute(f"INSERT INTO {table_name} (scale, note, date_time) VALUES (?, ?, ?)",
        (scale, note, date_time))
    conn.commit()
    cur.close()

def read_data (db_name, table_name, num_of_records):
    conn = open_db (db_name)
    cur = conn.cursor()
    sqlite_select_query = f"SELECT * from {table_name}"
    cur.execute(sqlite_select_query)
    data_list = cur.fetchall()
    cur.close()

    total_enteries = len(data_list)
    if total_enteries > num_of_records and num_of_records != 0:    #if you set number to 0, then you get them all.
        num_entry = num_of_records * -1
    else:
        num_entry = total_enteries * -1 

    full_string = []
    for i in range (num_entry, 0):
        sub_string = f'{datetime.fromtimestamp (data_list[i][3]):%a at %-I:%M} ({data_list[i][1]}) {data_list[i][2]}'
        full_string.append(sub_string)
    return full_string # list of strings

def day_num (date_time):  #datetime stamp
    # print(f'{date_time = } of type {type(date_time)}')
    return int(f'{datetime.fromtimestamp (date_time):%j}')

def day_num_convert (day_number):

    # print day number
    # print("The day number : " + str(day_number))
    day_num = str(day_number)

    # adjusting day num
    day_num.rjust(3 + len(day_num), '0')

    # Initialize year
    year = "2024"

    # converting to date
    res = datetime.strptime(year + "-" + day_num, "%Y-%j").strftime("%a %m-%d-%Y")

    # printing result
    return res


def tally_data (db_name, table_name):
    conn = open_db (db_name)
    cur = conn.cursor()
    sqlite_select_query = f"SELECT * from {table_name}"
    cur.execute(sqlite_select_query)
    data_list = cur.fetchall()
    cur.close()

    # total_enteries = len(data_list)
    first_day = day_num (data_list [0][3])
    last_day = day_num (data_list [-1][3])
    tally = []
    working_day = first_day
    total = 0
    # print (f'{tally = }')
    for day in data_list:
        # print (f'id {day[0]} scale {day[1]} day: {day_num (day [3])}')
        new_day = day_num (day [3])
        # print (f' if {new_day=} equals {working_day=}')
        if new_day == working_day:
            total = total + day [1]
            # print (f"{new_day=} {working_day=} {total=} {n=} and {average=} \n")
        else:
            # print (f'==========NEW DAY==============\n')
            # print (f'NEW DAY!!!! --> {new_day=} so append with {working_day=} {average=}')
            wd_readable = day_num_convert (working_day)
            tally.append ({'day': wd_readable, 'total': total})
            working_day = new_day
            total = day [1]
    # print (f'==========C DAY==============\n')
    # print (f'Last DAY!!!! --> {new_day=} so append with {working_day=} {average=}')
    wd_readable = day_num_convert (working_day)
    tally.append ({'day': wd_readable, 'total': total})

        # print (f'{day_number = }')
    
    full_string = []
    for t in tally:
        # sub_string = f"{t['average'] = } or {t['day'] = }"
        sub_string = f"{t['day']} {t['total']}"
        full_string.append(sub_string)
        # print (f"{t['average'] = } or {t['day'] = }")

    # for key, value in tally.items():
    #     print(key, ":", value)

    # for t in tally:
        # print('\n'.join([f"{key}: {values}" for key, values in t.items()]))

    return full_string

if __name__ == '__main__':
    DATABASE_NAME = 'Thoughts'
    DATABASE_TABLE = 'ideas'
    currentDateTime = datetime.now().timestamp()
    # print (day_num (currentDateTime))

    #create_db (DATABASE_NAME, DATABASE_TABLE)

    print (read_data (DATABASE_NAME, DATABASE_TABLE, 0))

    #write_data (DATABASE_NAME, DATABASE_TABLE, 10, "over by the fence", currentDateTime)

    # print (tally_data (DATABASE_NAME, DATABASE_TABLE))
    # print (day_num_convert(39))  # test for day_num_convert

    #proper end of python
    sys.exit(1)
