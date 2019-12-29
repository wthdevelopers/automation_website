"""
Runs tests on endpoints, assuming:
1. mysql server is running separately
2. backend server is running with FLASK_ENV environmen variable as "RemoteTest"
"""
import sys, os, pymysql.cursors, requests, datetime

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../')
sys.path.insert(0, filename)
from config import RemoteTest

BACKEND_URL = "http://127.0.0.1:5000"
PyMySQL = pymysql.connect(
    host=RemoteTest.HOST,
    user=RemoteTest.USER,
    password=RemoteTest.PW,
    db=RemoteTest.DB_NAME,
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor
)

pass_count = 0
test_count = 0

def clean_all_tables():
    """
    Revert all tables to start state
    """
    with PyMySQL.cursor() as cursor:
        cursor.execute("DELETE FROM comm")
        cursor.execute("DELETE FROM event")
        cursor.execute("DELETE FROM event_comm")
        cursor.execute("DELETE FROM grp")
        cursor.execute("DELETE FROM tool")
        cursor.execute("DELETE FROM user")
    PyMySQL.commit()

def index_of_string_difference(first, second):
    """
    Prints out difference in string

    Not used in actual test, only used when creating test cases
    """
    if len(first) >= len(second):
        length = len(second)
    else:
        length = len(first)
    print("first string length: {0}, second string length: {1}".format(len(first), len(second)))
    for i in range(length):
        if ord(first[i]) != ord(second[i]):
            print("index of difference: {0}, first string char: {1}, second string char: {2}".format(i, first[i], second[i]))

"""
### /functions/upcoming_events - positive test
# insert new row and retrieve id of new row
date_today = datetime.date.today().isoformat()
with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO event (name, start, end, place, description) VALUES ('event name 1', '{0} 13:13:13', '{1} 13:13:13', 'cc10', 'event description 1')".format(date_today, date_today))
    cursor.execute("SELECT LAST_INSERT_ID();")
    query_result = cursor.fetchall()
PyMySQL.commit()
row_index = query_result[0]["LAST_INSERT_ID()"]
print("value: {0}, datatype: {1}".format(row_index, type(row_index)))

# retrieve response from endpoint
response = requests.get(BACKEND_URL+"/functions/upcoming_events")
print(response.content)
value = response.content.decode("utf-8")

# comparison
# rgd the odd string formatting: https://stackoverflow.com/questions/2755201/str-format-raises-keyerror
to_compare = '{{"_upcoming_events_count":1,"upcoming_events":[{{"event_id":{0},"event_location":"cc10","event_name":"event name 1","event_time":{{"end_date":"{1}","end_time":"13:13","start_date":"{1}","start_time":"13:13"}}}}]}}\n'.format(row_index, date_today)
if value == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("test failed: /functions/upcoming_events - positive test")
    test_count += 1

clean_all_tables()


### /functions/find_participants - positive test
with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO grp (gname, space, categories) VALUES ('group name 1', 'cc10', 'yes')")
    cursor.execute("SELECT LAST_INSERT_ID();")
    new_group_id = cursor.fetchall()[0]["LAST_INSERT_ID()"]
PyMySQL.commit()

with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO user (name, contact_number, email, gid, participating) VALUES ('user 1', '91234567', 'test.email.com', {0}, 1)".format(new_group_id))
    cursor.execute("SELECT LAST_INSERT_ID();")
    new_user_id = cursor.fetchall()[0]["LAST_INSERT_ID()"]
PyMySQL.commit()

response = requests.get(BACKEND_URL+"/functions/find_participants", params={"participant_name":"user"}).content.decode("utf-8")
to_compare = '{{"_participants_count":1,"find_participants":[{{"participant_contact":"91234567","participant_id":{0},"participant_name":"user 1","participant_team_location":"cc10","participant_team_name":"group name 1"}}]}}\n'.format(new_user_id)
if response == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("test failed: /functions/find_participants - positive test")
    index_of_string_difference(response, to_compare)
    test_count += 1

clean_all_tables()
"""




print("{0}/{1} test cases passed.".format(pass_count, test_count))
