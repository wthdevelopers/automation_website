from openpyxl import load_workbook
import pymysql as pms

import sys, os
dirname = os.path.dirname(__file__)
sys.path.append(os.path.join(dirname, "../backend"))
from config import Production, RemoteTest


fname = 'test_data.xlsx'
ENV = RemoteTest

wb = load_workbook(filename=fname)
participant_data = wb['Sheet1']
headers = ('name',
           'DoB',
           'gender',
           'nationality',
           'email',
           'contact_number',
           'category_of_interest',
           'technology_of_interest',
           'skills',
           'organisation',
           'designation',
           'dietary_pref',
           'NoK_name',
           'NoK_relationship',
           'NoK_contact_number',
           'participating',
           'group_id')

conn = pms.connect(host=ENV.HOST,
                   user=ENV.USER,
                   password=ENV.PW,
                   db=ENV.DB_NAME)
conn.autocommit(True)

errors = []

sql_insert_query_template = 'INSERT INTO `user` ({}) VALUES ({})'
sql_cols = ','.join(['`{}`'.format(i) for i in headers])
for i, row in enumerate(participant_data):
    if i > 0:   # First row is headers
        sql_values = tuple(cell.value for cell in row[5:]) + (False, None) # First 5 columns not necessary
        sql_string_vals = ','.join('%s' for _ in sql_values)
        sql_insert_query = sql_insert_query_template.format(sql_cols, sql_string_vals)
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql_insert_query, sql_values)
            conn.commit()
        except Exception as e:
            errors.append(e)

conn.close()
print("errors: {0}".format(errors))

