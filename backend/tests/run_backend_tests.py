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
    cursorclass=pymysql.cursors.DictCursor,
    autocommit=True
)

pass_count = 0
test_count = 0

def clean_all_tables():
    """
    Revert all tables to start state
    """
    with PyMySQL.cursor() as cursor:
        cursor.execute("DELETE FROM user")
        cursor.execute("DELETE FROM duty_roster")
        cursor.execute("DELETE FROM event")
        cursor.execute("DELETE FROM consumable")
        cursor.execute("DELETE FROM consumable_group")
        cursor.execute("DELETE FROM `group`")
        cursor.execute("DELETE FROM tool")
        cursor.execute("DELETE FROM competition_category")
        cursor.execute("DELETE FROM category_group")
        cursor.execute("DELETE FROM score")
    

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


### /functions/upcoming_events - positive test
# insert new row and retrieve id of new row
date_today = datetime.date.today().isoformat()
with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO event (name, start_datetime, end_datetime, place, description) VALUES ('event name 1', '{0} 13:13:13', '{1} 13:13:13', 'cc10', 'event description 1')".format(date_today, date_today))
    cursor.execute("SELECT @last_uuid")
    new_event_id = cursor.fetchall()[0]["@last_uuid"]


# retrieve response from endpoint
response = requests.get(BACKEND_URL+"/functions/upcoming_events").content.decode("utf-8")

# comparison
# rgd the odd string formatting: https://stackoverflow.com/questions/2755201/str-format-raises-keyerror
to_compare = '{{"_upcoming_events_count":1,"upcoming_events":[{{"event_id":"{0}","event_location":"cc10","event_name":"event name 1","event_time":{{"end_date":"{1}","end_time":"13:13","start_date":"{1}","start_time":"13:13"}}}}]}}\n'.format(new_event_id, date_today)
if response == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("test failed: /functions/upcoming_events - positive test")
    print("response: {0}".format(response))
    print("to_compare: {0}".format(to_compare))
    # index_of_string_difference(response, to_compare)
    test_count += 1

clean_all_tables()



### /functions/find_participants - positive test
with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO `group` (name, space, categories) VALUES ('group name 1', 'cc10', 'yes')")
    cursor.execute("SELECT @last_uuid;")
    new_group_id = cursor.fetchall()[0]["@last_uuid"]


with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO user (name, contact_number, email, group_id, participating, DoB, gender, nationality, category_of_interest, skills, organisation, designation, NoK_contact_number) VALUES ('user 1', '91234567', 'test.email.com', '{0}', 1, '2020-01-01', 'male', 'singapore', 'category 1', 'skill 1', 'SUTD', 'software engineer', '90000001')".format(new_group_id))
    cursor.execute("SELECT @last_uuid;")
    new_user_id = cursor.fetchall()[0]["@last_uuid"]


response = requests.get(BACKEND_URL+"/functions/find_participants", params={"participant_name":"user"}).content.decode("utf-8")
to_compare = '{{"_participants_count":1,"find_participants":[{{"participant_contact":"91234567","participant_id":"{0}","participant_name":"user 1","participant_team_location":"cc10","participant_team_name":"group name 1"}}]}}\n'.format(new_user_id)
if response == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("test failed: /functions/find_participants - positive test")
    print("response: {0}".format(response))
    print("to_compare: {0}".format(to_compare))
    # index_of_string_difference(response, to_compare)
    test_count += 1

clean_all_tables()



### /ocomm/get_all - positive test
with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO comm (name, contact) VALUES ('ocomm name 1', '91234567')")
    cursor.execute("SELECT @last_uuid;")
    new_ocomm_id = cursor.fetchall()[0]["@last_uuid"]


date_today = datetime.date.today().isoformat()
with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO duty_roster (activity_name, start_datetime, end_datetime, place, description) VALUES ('event name 1', '{0} 13:13:13', '{0} 13:13:13', 'cc10', 'event description 1')".format(date_today))
    cursor.execute("SELECT @last_uuid;")
    new_roster_id = cursor.fetchall()[0]["@last_uuid"]


with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO duty_roster_comm (roster_id, comm_id) VALUES ('{0}', '{1}')".format(new_roster_id, new_ocomm_id,))


response = requests.get(BACKEND_URL+"/ocomm/get_all").content.decode("utf-8")
to_compare = '{{"_ocomm_count":1,"find_ocomm":[{{"ocomm_contact":"91234567","ocomm_current_location":"cc10","ocomm_current_shift_time":{{"end_date":"{0}","end_time":"13:13","start_date":"{0}","start_time":"13:13"}},"ocomm_id":"{1}","ocomm_name":"ocomm name 1"}}]}}\n'.format(date_today, new_ocomm_id)
if response == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("test failed: /ocomm/get_all - positive test")
    index_of_string_difference(response, to_compare)
    test_count += 1

clean_all_tables()



### /participants/register - positive test
with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO user (name, contact_number, email, group_id, participating, DoB, gender, nationality, category_of_interest, skills, organisation, designation, NoK_contact_number) VALUES ('user 1', '91234567', 'test.email.com', '0', 1, '2020-01-01', 'male', 'singapore', 'category 1', 'skill 1', 'SUTD', 'software engineer', '90000001')")
    cursor.execute("SELECT @last_uuid;")
    new_user_id = cursor.fetchall()[0]["@last_uuid"]

response = requests.put(BACKEND_URL+"/participants/register", params={"participant_id":"{0}".format(new_user_id)}).content.decode("utf-8")

with PyMySQL.cursor() as cursor:
    cursor.execute("SELECT participating FROM user WHERE user_id='{0}'".format(new_user_id))
    query_result = cursor.fetchall()

to_compare = 1
if query_result[0]["participating"] == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("test failed: /participants/register - positive test")
    index_of_string_difference(response, to_compare)
    test_count += 1

clean_all_tables()



### /participant/get_one - positive test
with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO `group` (name, space, categories) VALUES ('group name 1', 'cc10', 'yes')")
    cursor.execute("SELECT @last_uuid;")
    new_group_id = cursor.fetchall()[0]["@last_uuid"]

with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO user (name, contact_number, email, group_id, participating, DoB, gender, nationality, category_of_interest, skills, organisation, designation, NoK_contact_number) VALUES ('user 1', '90000001', 'test1.email.com', '{0}', 1, '2020-01-01', 'male', 'singapore', 'category 1', 'skill 1', 'SUTD', 'software engineer', '90000001')".format(new_group_id))
    cursor.execute("SELECT @last_uuid;")
    new_user1_id = cursor.fetchall()[0]["@last_uuid"]

with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO user (name, contact_number, email, group_id, participating, DoB, gender, nationality, category_of_interest, skills, organisation, designation, NoK_contact_number) VALUES ('user 2', '90000002', 'test2.email.com', '{0}', 1, '2020-01-01', 'male', 'singapore', 'category 1', 'skill 1', 'SUTD', 'software engineer', '90000002')".format(new_group_id))
    cursor.execute("SELECT @last_uuid;")
    new_user2_id = cursor.fetchall()[0]["@last_uuid"]

response = requests.get(BACKEND_URL+"/participants/get_one", params={"participant_id":"{0}".format(new_user1_id)}).content.decode("utf-8")

clean_all_tables()


print("{0}/{1} test cases passed.".format(pass_count, test_count))
