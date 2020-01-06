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
        cursor.execute("DELETE FROM category_group")
        cursor.execute("DELETE FROM comm")
        cursor.execute("DELETE FROM competition_category")
        cursor.execute("DELETE FROM consumable")
        cursor.execute("DELETE FROM consumable_group")
        cursor.execute("DELETE FROM duty_roster")
        cursor.execute("DELETE FROM duty_roster_comm")
        cursor.execute("DELETE FROM event")
        cursor.execute("DELETE FROM `group`")
        cursor.execute("DELETE FROM loan")
        cursor.execute("DELETE FROM score")
        cursor.execute("DELETE FROM tool")
        cursor.execute("DELETE FROM user")
    

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
    cursor.execute("INSERT INTO event (name, start_datetime, end_datetime, place, description) VALUES ('event name 1', '{0} 13:13:13', '{1} 13:13:13', 'cc10', 'description 1')".format(date_today, date_today))
    cursor.execute("SELECT @last_uuid")
    new_event_id = cursor.fetchall()[0]["@last_uuid"]

response = requests.get(BACKEND_URL+"/functions/upcoming_events").content.decode("utf-8")

# rgd the odd string formatting: https://stackoverflow.com/questions/2755201/str-format-raises-keyerror
to_compare = '{{"_upcoming_events_count":1,"functions_upcoming_events":[{{"event_id":"{0}","event_location":"cc10","event_name":"event name 1","event_time":{{"end_date":"{1}","end_time":"13:13","start_date":"{1}","start_time":"13:13"}}}}]}}\n'.format(new_event_id, date_today)
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
    cursor.execute("INSERT INTO user (name, contact_number, email, group_id, participating, DoB, gender, nationality, category_of_interest, technology_of_interest, skills, organisation, designation, dietary_pref, NoK_name, NoK_relationship, NoK_contact_number) VALUES ('user 1', '91234567', 'test.email.com', '{0}', 1, '2020-01-01', 'male', 'singapore', 'category 1', 'technology of interest 1', 'skill 1', 'SUTD', 'software engineer', 'dietary_pref 1', 'NoK name 1', 'NoK relationship 1', '90000001')".format(new_group_id))
    cursor.execute("SELECT @last_uuid;")
    new_user_id = cursor.fetchall()[0]["@last_uuid"]


response = requests.get(BACKEND_URL+"/functions/find_participants", params={"participant_name":"user"}).content.decode("utf-8")
to_compare = '{{"_participants_count":1,"functions_find_participants":[{{"participant_contact":"91234567","participant_id":"{0}","participant_name":"user 1","participant_team_location":"cc10","participant_team_name":"group name 1"}}]}}\n'.format(new_user_id)
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



### /participants/register - positive test
with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO user (name, contact_number, email, group_id, participating, DoB, gender, nationality, category_of_interest, technology_of_interest, skills, organisation, designation, dietary_pref, NoK_name, NoK_relationship, NoK_contact_number) VALUES ('user 1', '91234567', 'test.email.com', '{0}', 1, '2020-01-01', 'male', 'singapore', 'category 1', 'technology of interest 1', 'skill 1', 'SUTD', 'software engineer', 'dietary_pref 1', 'NoK name 1', 'NoK relationship 1', '90000001')".format(new_group_id))
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



### /participants/get_one - positive test
with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO `group` (name, space, categories) VALUES ('group name 1', 'cc10', 'yes')")
    cursor.execute("SELECT @last_uuid;")
    new_group_id = cursor.fetchall()[0]["@last_uuid"]

with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO user (name, contact_number, email, group_id, participating, DoB, gender, nationality, category_of_interest, technology_of_interest, skills, organisation, designation, dietary_pref, NoK_name, NoK_relationship, NoK_contact_number) VALUES ('user 1', '91234567', 'test.email.com', '{0}', 1, '2020-01-01', 'male', 'singapore', 'category 1', 'technology of interest 1', 'skill 1', 'SUTD', 'software engineer', 'dietary_pref 1', 'NoK name 1', 'NoK relationship 1', '90000001')".format(new_group_id))
    cursor.execute("SELECT @last_uuid;")
    new_user1_id = cursor.fetchall()[0]["@last_uuid"]

with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO user (name, contact_number, email, group_id, participating, DoB, gender, nationality, category_of_interest, technology_of_interest, skills, organisation, designation, dietary_pref, NoK_name, NoK_relationship, NoK_contact_number) VALUES ('user 2', '91234567', 'test.email.com', '{0}', 2, '2020-01-01', 'male', 'singapore', 'category 2', 'technology of interest 2', 'skill 2', 'SUTD', 'software engineer', 'dietary_pref 2', 'NoK name 2', 'NoK relationship 2', '90000002')".format(new_group_id))
    cursor.execute("SELECT @last_uuid;")
    new_user2_id = cursor.fetchall()[0]["@last_uuid"]

response = requests.get(BACKEND_URL+"/participants/get_one", params={"participant_id":"{0}".format(new_user1_id)}).content.decode("utf-8")

to_compare = '{{"participants_get_one":{{"_team_member_number":1,"participant_details":{{"participant_contact":"91234567","participant_id":"{0}","participant_name":"user 1","participant_team_location":"cc10"}},"participant_team_name":"group name 1","team_member_details":[{{"participant_contact":"91234567","participant_id":"{1}","participant_name":"user 2","participant_team_location":"cc10"}}]}}}}\n'.format(new_user1_id, new_user2_id)

if response == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("response: \n{0}".format(response))
    print("to_compare: \n{0}".format(to_compare))
    print("test failed: /participants/get_one - positive test")
    index_of_string_difference(response, to_compare)
    test_count += 1

clean_all_tables()



### /item_loans/get_all - positive test
with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO user (name, contact_number, email, group_id, participating, DoB, gender, nationality, category_of_interest, technology_of_interest, skills, organisation, designation, dietary_pref, NoK_name, NoK_relationship, NoK_contact_number) VALUES ('user 1', '91234567', 'test.email.com', '0', 1, '2020-01-01', 'male', 'singapore', 'category 1', 'technology of interest 1', 'skill 1', 'SUTD', 'software engineer', 'dietary_pref 1', 'NoK name 1', 'NoK relationship 1', '90000001');")
    cursor.execute("SELECT @last_uuid;")
    new_user_id = cursor.fetchall()[0]["@last_uuid"]

with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO `tool` (status, name) VALUES ('not returned', 'tool name 1');".format(new_user_id))
    cursor.execute("SELECT @last_uuid;")
    new_tool1_id = cursor.fetchall()[0]["@last_uuid"]

with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO `tool` (status, name) VALUES ('returned', 'tool name 2');".format(new_user_id))
    cursor.execute("SELECT @last_uuid;")
    new_tool2_id = cursor.fetchall()[0]["@last_uuid"]

with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO `loan` (tool_id, loan_to_user_id, loan_datetime) VALUES ('{0}', '{1}', '2020-01-01 10:13:13');".format(new_tool1_id, new_user_id))
    cursor.execute("INSERT INTO `loan` (tool_id, loan_to_user_id, loan_datetime) VALUES ('{0}', '{1}', '2020-01-01 13:13:13');".format(new_tool1_id, new_user_id))
    cursor.execute("SELECT @last_uuid;")
    new_loan1_id = cursor.fetchall()[0]["@last_uuid"]

with PyMySQL.cursor() as cursor:
    cursor.execute("UPDATE tool SET latest_loan='{0}' WHERE tool_id='{1}';".format(new_loan1_id, new_tool1_id))

response = requests.get(BACKEND_URL+"/item_loans/get_all").content.decode("utf-8")

to_compare = '{{"_item_count":2,"item_loans_get_all":[{{"on_loan_to":"user 1","status":"not returned","tool_id":"{0}","tool_name":"tool name 1"}},{{"on_loan_to":null,"status":"returned","tool_id":"{1}","tool_name":"tool name 2"}}]}}\n'.format(new_tool1_id, new_tool2_id)

if response == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("response: \n{0}".format(response))
    print("to_compare: \n{0}".format(to_compare))
    print("test failed: /participants/get_one - positive test")
    index_of_string_difference(response, to_compare)
    test_count += 1

clean_all_tables()



### event/delay_multiple - positive test
with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO event (name, start_datetime, end_datetime, place) VALUES ('activity_1', '2020-01-01 00:00:00', '2020-01-01 10:00:00', 'cc10');")
    cursor.execute("SELECT @last_uuid;")
    new_duty_event1_id = cursor.fetchall()[0]["@last_uuid"]

with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO event (name, start_datetime, end_datetime, place) VALUES ('activity_2', '2020-01-01 10:00:00', '2020-01-01 12:00:00', 'cc10');")
    cursor.execute("SELECT @last_uuid;")
    new_duty_event2_id = cursor.fetchall()[0]["@last_uuid"]

request_body = {"schedule_editor/delay": {"event_id_list": [new_duty_event1_id, new_duty_event2_id],"delay_by_minutes": 50}}
response = requests.put(BACKEND_URL+"/event/delay_multiple", json=request_body).content.decode("utf-8")

with PyMySQL.cursor() as cursor:
    cursor.execute("SELECT start_datetime, end_datetime FROM event WHERE event_id='{0}'".format(new_duty_event1_id))
    query_results = cursor.fetchall()[0]
    new_start_datetime_1 = query_results["start_datetime"].isoformat()
    new_end_datetime_1 = query_results["end_datetime"].isoformat()

with PyMySQL.cursor() as cursor:
    cursor.execute("SELECT start_datetime, end_datetime FROM event WHERE event_id='{0}'".format(new_duty_event2_id))
    query_results = cursor.fetchall()[0]
    new_start_datetime_2 = query_results["start_datetime"].isoformat()
    new_end_datetime_2 = query_results["end_datetime"].isoformat()

response = "new_start_datetime_1: {0}, new_end_datetime_1: {1}, new_start_datetime_2: {2}, new_end_datetime_2: {3}".format(new_start_datetime_1, new_end_datetime_1, new_start_datetime_2, new_end_datetime_2)

to_compare = "new_start_datetime_1: 2020-01-01T00:50:00, new_end_datetime_1: 2020-01-01T10:50:00, new_start_datetime_2: 2020-01-01T10:50:00, new_end_datetime_2: 2020-01-01T12:50:00"

if response == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("response: \n{0}".format(response))
    print("to_compare: \n{0}".format(to_compare))
    print("test failed: /event/delay_multiple - positive test")
    index_of_string_difference(response, to_compare)
    test_count += 1

clean_all_tables()



### event/add_one - positive test
request_body = { \
    "schedule_editor/add": { \
        "event_time": { \
            "start_time": "17:00", \
            "start_date": "2020-12-13", \
            "end_time": "18:30", \
            "end_date": "2020-12-13" \
        }, \
        "event_name": "Hacking Activity 01", \
        "event_location": "CC14", \
        "event_description": "event description 1" \
    } \
}
response = requests.post(BACKEND_URL+"/event/add_one", json=request_body).content.decode("utf-8")

with PyMySQL.cursor() as cursor:
    cursor.execute("SELECT name FROM event;")
    new_event_name = cursor.fetchall()[0]["name"]

response = "new_event_name: {0}".format(new_event_name)

to_compare = "new_event_name: Hacking Activity 01"

if response == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("response: \n{0}".format(response))
    print("to_compare: \n{0}".format(to_compare))
    print("test failed: /event/add_one - positive test")
    index_of_string_difference(response, to_compare)
    test_count += 1

clean_all_tables()



### event/edit_one - positive test
with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO event (name, start_datetime, end_datetime, place, description) VALUES ('activity name 1', '2020-12-13 00:00:00', '2020-12-13 10:00:00', 'CC10', 'description 1')")
    cursor.execute("SELECT @last_uuid;")
    new_event_id = cursor.fetchall()[0]["@last_uuid"]

request_body = { \
    "event_edit_one": { \
        "event_time": { \
            "start_time": "17:00", \
            "start_date": "2020-12-13", \
            "end_time": "18:30", \
            "end_date": "2020-12-13" \
        }, \
        "event_name": "Hacking Activity 01 NEW", \
        "event_location": "CC14", \
        "event_description": "event description 1" \
    } \
}
response = requests.put(BACKEND_URL+"/event/edit_one", params={"event_id": new_event_id}, json=request_body).content.decode("utf-8")

with PyMySQL.cursor() as cursor:
    cursor.execute("SELECT name FROM event WHERE event_id='{0}';".format(new_event_id))
    new_event_name = cursor.fetchall()[0]["name"]

response = "new_event_name: {0}".format(new_event_name)

to_compare = "new_event_name: Hacking Activity 01 NEW"

if response == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("response: \n{0}".format(response))
    print("to_compare: \n{0}".format(to_compare))
    print("test failed: /event/edit_one - positive test")
    index_of_string_difference(response, to_compare)
    test_count += 1

clean_all_tables()



### event/delete_one - positive test
with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO event (name, start_datetime, end_datetime, place, description) VALUES ('activity name 1', '2020-12-13 00:00:00', '2020-12-13 10:00:00', 'CC10', 'description 1')")
    cursor.execute("SELECT @last_uuid;")
    new_event_id = cursor.fetchall()[0]["@last_uuid"]

with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO event (name, start_datetime, end_datetime, place, description) VALUES ('activity name 2', '2020-12-13 00:00:00', '2020-12-13 10:00:00', 'CC10', 'description 2')")

response = requests.delete(BACKEND_URL+"/event/delete_one", params={"event_id": new_event_id}).content.decode("utf-8")

with PyMySQL.cursor() as cursor:
    cursor.execute("SELECT name FROM event;")
    response = cursor.fetchall()

to_compare = [{'name': 'activity name 2'}]

if response == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("response: \n{0}".format(response))
    print("to_compare: \n{0}".format(to_compare))
    print("test failed: /event/delete_one - positive test")
    index_of_string_difference(response, to_compare)
    test_count += 1

clean_all_tables()


print("{0}/{1} test cases passed.".format(pass_count, test_count))
