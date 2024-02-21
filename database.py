#!/usr/bin/python
from datetime import datetime
import sqlite3
from sqlite3 import Error
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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
    # print ('file opened')
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

# def read_data (db_name, table_name, num_of_records):
def read_data (db_name, table_name, **kwargs):
    conn = open_db (db_name)
    cur = conn.cursor()
    sqlite_select_query = f"SELECT * from {table_name}"
    cur.execute(sqlite_select_query)
    data_list = cur.fetchall()
    cur.close()

    num_of_records = kwargs.get('num_of_records',0)
    total_enteries = len(data_list)
    if total_enteries > num_of_records and num_of_records != 0:    #if you set number to 0, then you get them all.
        num_entry = num_of_records * -1
    else:
        num_entry = total_enteries * -1 

    if kwargs.get('output', None) == "list":
        output_list = []
        ind = 0
        for i in range (num_entry, 0):
            ind += 1
            day_string = f'{datetime.fromtimestamp (data_list[i][3]):%a %m-%d-%Y}'
            sub_string = {'day': day_string,
                          'scale': data_list[i][1],
                           'note': data_list[i][2]}
            output_list.append(sub_string)
        return output_list # list if dict

    else:
        full_string = [] 
        ind = 0
        for i in range (num_entry, 0):
            ind += 1
            sub_string = f'{ind} ~ {datetime.fromtimestamp (data_list[i][3]):%a at %-I:%M} ({data_list[i][1]}) {data_list[i][2]}'
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

def tally_data (db_name, table_name, **kwargs):
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
    
    # print (f'{output = }')
    # output_type = kwargs.get('output', None)
    # print (f'{output_type = }')
    if kwargs.get('output', None) == "list":
        # print ("list was chosen")
        return tally # list

    else:
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

def journal (db_name, table_name, **kwargs):
    tally_data_list = tally_data (DATABASE_NAME, DATABASE_TABLE, output ='list')
    full_database = read_data (DATABASE_NAME, DATABASE_TABLE, output = 'list')
    account = []
    for tdl in tally_data_list:
        day_info = tdl.get ('day')
        # print (f'{day_info = }')
        day_notes = []
        for fd in full_database:
            if day_info == fd.get('day'):
                # print (f'{fd = }')
                day_notes.append(fd)
        day_account = {'notes': day_notes, 'totals': tdl}
        account.append(day_account)

    return account


if __name__ == '__main__':
    DATABASE_NAME = '/home/michael/Desktop/iPhone/Thoughts'
    DATABASE_TABLE = 'ideas'
    currentDateTime = datetime.now().timestamp()
    # print (day_num (currentDateTime))

    #create_db (DATABASE_NAME, DATABASE_TABLE)

    # print (read_data (DATABASE_NAME, DATABASE_TABLE, num_of_records = 5, output = 'list'))
    # print (read_data (DATABASE_NAME, DATABASE_TABLE, ))

    #write_data (DATABASE_NAME, DATABASE_TABLE, 10, "over by the fence", currentDateTime)

    # print (tally_data (DATABASE_NAME, DATABASE_TABLE,))
    # print (tally_data (DATABASE_NAME, DATABASE_TABLE, output ='list'))
    # print (day_num_convert(39))  # test for day_num_convert

    total_acounting = journal (DATABASE_NAME, DATABASE_TABLE,)
    total_entry_number = 0
    total_scale = 0
    num_of_days = 0
    graph_list = []
    for accounting in  total_acounting:
        # print (f'{accounting = } \n\n')
        num_of_days += 1
        totals = accounting.get ('totals')
        report_date = totals.get('day')
        date_totals = totals.get('total')
        graph_daily = {}
        # print (f'For the date of {report_date}')
        notes = accounting.get ('notes')
        num_of_entry = 0
        daily_scale = 0
        for note in notes:
            num_of_entry += 1
            note_string = note.get('note')
            scale = note.get('scale')
            # print (f'scale/score is {scale} - {note_string}')
            daily_scale = daily_scale + scale
        total_entry_number = total_entry_number + num_of_entry
        total_scale = total_scale + daily_scale
        graph_daily = {'date': report_date, 'scale': daily_scale, 'entries': num_of_entry}
        # print (f'Total scale/score of {date_totals} on {num_of_entry} entries \n\n')
        graph_list.append(graph_daily)
    print (f'Total number of enteries {total_entry_number} and a total scale of {total_scale}')
    print (f'meaning a daily average scale of {total_scale / num_of_days:.1f} on {total_entry_number / num_of_days:.1f} entries per day.')

    #proper end of python

    # print (f'{graph_list = }')
    # array = np.array(graph_list)
    # print (array)
    df = pd.DataFrame(graph_list)
    # print (df['date'], [df['scale'], df['entries']])
    df['scale_average'] = df.rolling(5).mean()
    df.plot('date', ['scale', 'entries'] )
    plt.show()


    sys.exit()
