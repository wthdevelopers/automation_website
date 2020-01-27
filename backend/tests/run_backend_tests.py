"""
Runs tests on endpoints, assuming:
1. mysql server is running separately
2. backend server is running with FLASK_ENV environmen variable as "RemoteTest"
"""
import sys, os, pymysql.cursors, requests, datetime
from flask import json

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
USERNAME = "username"
PASSWORD = "password"

pass_count = 0
test_count = 0

def clean_all_tables():
    """
    Revert all tables to start state
    """
    with PyMySQL.cursor() as cursor:
        cursor.execute("DELETE FROM category_group")
        cursor.execute("DELETE FROM competition_category")
        cursor.execute("DELETE FROM consumable")
        cursor.execute("DELETE FROM consumable_group")
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


def add_test_cred():
    """
    Adds sample username and password to RemoteTest
    """

    import hashlib

    salted_password = PASSWORD + RemoteTest.PW_SALT
    hashed_pw = hashlib.sha256(bytes(salted_password, "utf-8")).hexdigest()

    query = "INSERT INTO `credentials` (username, password) VALUES ('{0}', '{1}')".format(USERNAME, hashed_pw)

    with PyMySQL.cursor() as cursor:
        cursor.execute(query)


def remove_test_cred():
    """
    Delete all credentials from 'RemoteTest' db
    """

    query = "DELETE FROM `credentials`"

    with PyMySQL.cursor() as cursor:
        cursor.execute(query)



### authorization
add_test_cred()

login_session = requests.Session()
request_body = {"username": "username", "password": "password"}

response = login_session.post(BACKEND_URL+"/login", json=request_body).content.decode("utf-8")
before_login_response = login_session.get(BACKEND_URL+"/test", json=request_body).content.decode("utf-8")

response = login_session.get(BACKEND_URL+"/logout", json=request_body).content.decode("utf-8")
after_login_response = login_session.get(BACKEND_URL+"/test", json=request_body).content.decode("utf-8")

if before_login_response == "HELLO WORLD" and after_login_response == "Unauthorized":
    pass_count += 1
    test_count += 1
else:
    print("response: \n{0}".format(query_result))
    print("to_compare: \n{0}".format(to_compare))
    print("authorization - positive test")
    index_of_string_difference(query_result, to_compare)
    test_count += 1

response = login_session.post(BACKEND_URL+"/login", json=request_body).content.decode("utf-8")  # login for the rest of the endpoints


### /participants/ID/register - positive test
with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO user (name, contact_number, email, group_id, registered, DoB, gender, nationality, category_of_interest, technology_of_interest, skills, organisation, designation, dietary_pref, NoK_name, NoK_relationship, NoK_contact_number) VALUES ('user 1', '91234567', 'test.email.com', '1', 0, '2020-01-01', 'male', 'singapore', 'category 1', 'technology of interest 1', 'skill 1', 'SUTD', 'software engineer', 'dietary_pref 1', 'NoK name 1', 'NoK relationship 1', '90000001')")
    cursor.execute("SELECT @last_uuid;")
    new_user_id = cursor.fetchall()[0]["@last_uuid"]

response = login_session.put(BACKEND_URL+"/participants/{0}/register".format(new_user_id)).content.decode("utf-8")

with PyMySQL.cursor() as cursor:
    cursor.execute("SELECT registered FROM user WHERE user_id='{0}'".format(new_user_id))
    query_result = cursor.fetchall()

to_compare = 1
if query_result[0]["registered"] == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("test failed: /participants/register - positive test")
    index_of_string_difference(query_result[0]["registered"], to_compare)
    test_count += 1

clean_all_tables()



### /participants/ID/deregister - positive test
with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO user (name, contact_number, email, group_id, registered, DoB, gender, nationality, category_of_interest, technology_of_interest, skills, organisation, designation, dietary_pref, NoK_name, NoK_relationship, NoK_contact_number) VALUES ('user 1', '91234567', 'test.email.com', '1', 1, '2020-01-01', 'male', 'singapore', 'category 1', 'technology of interest 1', 'skill 1', 'SUTD', 'software engineer', 'dietary_pref 1', 'NoK name 1', 'NoK relationship 1', '90000001')")
    cursor.execute("SELECT @last_uuid;")
    new_user_id = cursor.fetchall()[0]["@last_uuid"]

response = login_session.put(BACKEND_URL+"/participants/{0}/deregister".format(new_user_id)).content.decode("utf-8")

with PyMySQL.cursor() as cursor:
    cursor.execute("SELECT registered FROM user WHERE user_id='{0}'".format(new_user_id))
    query_result = cursor.fetchall()

to_compare = 0
if query_result[0]["registered"] == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("test failed: /participants/ID/deregister - positive test")
    index_of_string_difference(response, to_compare)
    test_count += 1

clean_all_tables()



### /loans/get_all - positive test
with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO `group` (name, space) VALUES ('name 1', 'space 1')")
    cursor.execute("SELECT @last_uuid;")
    new_group_id = cursor.fetchall()[0]["@last_uuid"]

with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO `tool` (loaned, name) VALUES ('1', 'tool name 1');".format(new_user_id))
    cursor.execute("SELECT @last_uuid;")
    new_tool1_id = cursor.fetchall()[0]["@last_uuid"]

with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO `tool` (loaned, name) VALUES ('0', 'tool name 2');".format(new_user_id))
    cursor.execute("SELECT @last_uuid;")
    new_tool2_id = cursor.fetchall()[0]["@last_uuid"]

with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO `loan` (tool_id, loan_to_group_id, loan_datetime) VALUES ('{0}', '{1}', '2020-01-01 10:13:13');".format(new_tool1_id, new_group_id))
    cursor.execute("INSERT INTO `loan` (tool_id, loan_to_group_id, loan_datetime) VALUES ('{0}', '{1}', '2020-01-01 13:13:13');".format(new_tool1_id, new_group_id))
    cursor.execute("SELECT @last_uuid;")
    new_loan1_id = cursor.fetchall()[0]["@last_uuid"]

with PyMySQL.cursor() as cursor:
    cursor.execute("UPDATE tool SET latest_loan='{0}' WHERE tool_id='{1}';".format(new_loan1_id, new_tool1_id))

response = login_session.get(BACKEND_URL+"/loans/get_all").content.decode("utf-8")

to_compare = '{{"_tools_count":2,"loans_get_all":[{{"loaned":1,"on_loan_to":"name 1","tool_id":"{0}","tool_name":"tool name 1"}},{{"loaned":0,"on_loan_to":null,"tool_id":"{1}","tool_name":"tool name 2"}}]}}\n'.format(new_tool1_id, new_tool2_id)

if response == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("response: \n{0}".format(response))
    print("to_compare: \n{0}".format(to_compare))
    print("test failed: /loans/get_all - positive test")
    index_of_string_difference(response, to_compare)
    test_count += 1

clean_all_tables()



### /participants/get_all - positive test
with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO user (name, contact_number, email, group_id, registered, DoB, gender, nationality, category_of_interest, technology_of_interest, skills, organisation, designation, dietary_pref, NoK_name, NoK_relationship, NoK_contact_number) VALUES ('user 1', '91234567', 'test.email.com', '1', 1, '2020-01-01', 'male', 'singapore', 'category 1', 'technology of interest 1', 'skill 1', 'SUTD', 'software engineer', 'dietary_pref 1', 'NoK name 1', 'NoK relationship 1', '90000001')")
    cursor.execute("SELECT @last_uuid;")
    new_user1_id = cursor.fetchall()[0]["@last_uuid"]

with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO user (name, contact_number, email, group_id, registered, DoB, gender, nationality, category_of_interest, technology_of_interest, skills, organisation, designation, dietary_pref, NoK_name, NoK_relationship, NoK_contact_number) VALUES ('user 2', '91234567', 'test.email.com', '1', 2, '2020-01-01', 'male', 'singapore', 'category 2', 'technology of interest 2', 'skill 2', 'SUTD', 'software engineer', 'dietary_pref 2', 'NoK name 2', 'NoK relationship 2', '90000002')")
    cursor.execute("SELECT @last_uuid;")
    new_user2_id = cursor.fetchall()[0]["@last_uuid"]

response = login_session.get(BACKEND_URL+"/participants/get_all").content.decode("utf-8")
to_compare = '{{"_participants_count":2,"participants_all":[{{"id":"{0}","name":"user 1","registered":1}},{{"id":"{1}","name":"user 2","registered":2}}]}}\n'.format(new_user1_id, new_user2_id)

if response == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("response: \n{0}".format(response))
    print("to_compare: \n{0}".format(to_compare))
    print("test failed: /participants/get_all - positive test")
    index_of_string_difference(response, to_compare)
    test_count += 1

clean_all_tables()



### /participants/ID/alldata - positive test
with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO user (name, contact_number, email, group_id, registered, DoB, gender, nationality, category_of_interest, technology_of_interest, skills, organisation, designation, dietary_pref, NoK_name, NoK_relationship, NoK_contact_number) VALUES ('user 1', '91234567', 'test.email.com', '1', 1, '2020-01-01', 'male', 'singapore', 'category 1', 'technology of interest 1', 'skill 1', 'SUTD', 'software engineer', 'dietary_pref 1', 'NoK name 1', 'NoK relationship 1', '90000001')")
    cursor.execute("SELECT @last_uuid;")
    new_user1_id = cursor.fetchall()[0]["@last_uuid"]

response = login_session.get(BACKEND_URL+"/participants/{0}/alldata".format(new_user1_id)).content.decode("utf-8")
to_compare = '{{"participants_ID_alldata":[{{"DoB":"Wed, 01 Jan 2020 00:00:00 GMT","NoK_contact_number":"90000001","NoK_name":"NoK name 1","NoK_relationship":"NoK relationship 1","category_of_interest":"category 1","contact_number":"91234567","designation":"software engineer","dietary_pref":"dietary_pref 1","email":"test.email.com","gender":"male","group_id":"1","id":"{0}","name":"user 1","nationality":"singapore","organisation":"SUTD","registered":1,"skills":"skill 1","technology_of_interest":"technology of interest 1"}}]}}\n'.format(new_user1_id)

if response == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("response: \n{0}".format(response))
    print("to_compare: \n{0}".format(to_compare))
    print("test failed: /participants/ID/alldata - positive test")
    index_of_string_difference(response, to_compare)
    test_count += 1

clean_all_tables()



### /participants/ID/update - positive test
with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO user (name, contact_number, email, group_id, registered, DoB, gender, nationality, category_of_interest, technology_of_interest, skills, organisation, designation, dietary_pref, NoK_name, NoK_relationship, NoK_contact_number) VALUES ('user 1', '91234567', 'test.email.com', '1', 1, '2020-01-01', 'male', 'singapore', 'category 1', 'technology of interest 1', 'skill 1', 'SUTD', 'software engineer', 'dietary_pref 1', 'NoK name 1', 'NoK relationship 1', '90000001')")
    cursor.execute("SELECT @last_uuid;")
    user1_id = cursor.fetchall()[0]["@last_uuid"]

request_body = {
	"DoB":"2020-02-02 02:02:02",
	"NoK_contact_number":"90000002",
	"NoK_name":"NoK name 2",
	"NoK_relationship":"NoK relationship 2",
	"category_of_interest":"category 2",
	"contact_number":"91234568",
	"designation":"hustler",
	"dietary_pref":"dietary_pref 2",
	"email":"test.email.com.sg",
	"gender":"shemale",
	"group_id":"2",
	"name":"user 2",
	"nationality":"bangalore",
	"organisation":"STD",
	"registered":0,
	"skills":"skill 2",
	"technology_of_interest":"technology of interest 2"
}

response = login_session.put(BACKEND_URL+"/participants/{0}/update".format(user1_id), json=request_body).content.decode("utf-8")
to_compare = "[{{'user_id': '{0}', 'name': 'user 2', 'contact_number': '91234568', 'email': 'test.email.com.sg', 'group_id': '2', 'registered': 0, 'DoB': datetime.datetime(2020, 2, 2, 2, 2, 2), 'gender': 'shemale', 'nationality': 'bangalore', 'category_of_interest': 'category 2', 'technology_of_interest': 'technology of interest 2', 'skills': 'skill 2', 'organisation': 'STD', 'designation': 'hustler', 'dietary_pref': 'dietary_pref 2', 'NoK_name': 'NoK name 2', 'NoK_relationship': 'NoK relationship 2', 'NoK_contact_number': '90000002'}}]".format(user1_id)

with PyMySQL.cursor() as cursor:
    cursor.execute("SELECT * from user WHERE user_id='{0}';".format(user1_id))
    query_result = str(cursor.fetchall())

if query_result == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("response: \n{0}".format(query_result))
    print("to_compare: \n{0}".format(to_compare))
    print("test failed: /participants/ID/update - positive test")
    index_of_string_difference(query_result, to_compare)
    test_count += 1

clean_all_tables()



### /participants/ID/group - positive test - user does not exist

response = login_session.get(BACKEND_URL+"/participants/{0}/group".format("nonexistent-id"), json=request_body).content.decode("utf-8")
to_compare = '{"group_id":null,"user_exist":0}\n'
if response == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("response: \n{0}".format(query_result))
    print("to_compare: \n{0}".format(to_compare))
    print("test failed: /participants/ID/group - positive test - user does not exist")
    index_of_string_difference(query_result, to_compare)
    test_count += 1

clean_all_tables()



### /participants/ID/group - positive test - user exist, does not belong in a group
with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO user (name, contact_number, email, group_id, registered, DoB, gender, nationality, category_of_interest, technology_of_interest, skills, organisation, designation, dietary_pref, NoK_name, NoK_relationship, NoK_contact_number) VALUES ('user 1', '91234567', 'test.email.com', NULL, 0, '2020-01-01', 'male', 'singapore', 'category 1', 'technology of interest 1', 'skill 1', 'SUTD', 'software engineer', 'dietary_pref 1', 'NoK name 1', 'NoK relationship 1', '90000001')")
    cursor.execute("SELECT @last_uuid;")
    new_user_id = cursor.fetchall()[0]["@last_uuid"]
response = login_session.get(BACKEND_URL+"/participants/{0}/group".format(new_user_id), json=request_body).content.decode("utf-8")
to_compare = '{"group_id":null,"user_exist":1}\n'
if response == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("response: \n{0}".format(query_result))
    print("to_compare: \n{0}".format(to_compare))
    print("test failed: /participants/ID/group - positive test - user exist, does not belong in a group")
    index_of_string_difference(query_result, to_compare)
    test_count += 1

clean_all_tables()



### /participants/ID/group - positive test - user exist, belongs in a group
with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO user (name, contact_number, email, group_id, registered, DoB, gender, nationality, category_of_interest, technology_of_interest, skills, organisation, designation, dietary_pref, NoK_name, NoK_relationship, NoK_contact_number) VALUES ('user 1', '91234567', 'test.email.com', '1', 0, '2020-01-01', 'male', 'singapore', 'category 1', 'technology of interest 1', 'skill 1', 'SUTD', 'software engineer', 'dietary_pref 1', 'NoK name 1', 'NoK relationship 1', '90000001')")
    cursor.execute("SELECT @last_uuid;")
    new_user_id = cursor.fetchall()[0]["@last_uuid"]
response = login_session.get(BACKEND_URL+"/participants/{0}/group".format(new_user_id), json=request_body).content.decode("utf-8")
to_compare = '{"group_id":"1","user_exist":1}\n'
if response == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("response: \n{0}".format(query_result))
    print("to_compare: \n{0}".format(to_compare))
    print("test failed: /participants/ID/group - positive test - user exist, belongs in a group")
    index_of_string_difference(query_result, to_compare)
    test_count += 1

clean_all_tables()



### /consumables/get_all - positive test
with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO consumable (name, description, stock_qty, total_qty, quota_per_group) VALUES ('name 1', 'description 1', 4, 10, 1)")
    cursor.execute("SELECT @last_uuid;")
    new_consumable1_id = cursor.fetchall()[0]["@last_uuid"]

with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO consumable (name, description, stock_qty, total_qty, quota_per_group) VALUES ('name 2', 'description 2', 4, 10, 1)")
    cursor.execute("SELECT @last_uuid;")
    new_consumable2_id = cursor.fetchall()[0]["@last_uuid"]

response = login_session.get(BACKEND_URL+"/consumables/get_all").content.decode("utf-8")
to_compare = '{{"_consumables_count":2,"consumables_get_all":[{{"id":"{0}","name":"name 1","quota_per_group":1,"remaining_count":6}},{{"id":"{1}","name":"name 2","quota_per_group":1,"remaining_count":6}}]}}\n'.format(new_consumable1_id, new_consumable2_id)

if response == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("response: \n{0}".format(response))
    print("to_compare: \n{0}".format(to_compare))
    print("test failed: /consumables/get_all - positive test")
    index_of_string_difference(response, to_compare)
    test_count += 1

clean_all_tables()



### /groups/get_all - positive test
with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO `group` (name, space) VALUES ('name 1', 'space 1')")
    cursor.execute("SELECT @last_uuid;")
    new_group1_id = cursor.fetchall()[0]["@last_uuid"]

with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO `group` (name, space) VALUES ('name 2', 'space 2')")
    cursor.execute("SELECT @last_uuid;")
    new_group2_id = cursor.fetchall()[0]["@last_uuid"]

response = login_session.get(BACKEND_URL+"/groups/get_all").content.decode("utf-8")
to_compare = '{{"_groups_count":2,"groups_get_all":[{{"hacking_space":"space 1","id":"{0}","name":"name 1"}},{{"hacking_space":"space 2","id":"{1}","name":"name 2"}}]}}\n'.format(new_group1_id, new_group2_id)

if response == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("response: \n{0}".format(response))
    print("to_compare: \n{0}".format(to_compare))
    print("test failed: /groups/get_all - positive test")
    index_of_string_difference(response, to_compare)
    test_count += 1

clean_all_tables()



### /groups/ID/alldata - positive test
with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO `group` (name, space) VALUES ('name 1', 'space 1')")
    cursor.execute("SELECT @last_uuid;")
    new_group1_id = cursor.fetchall()[0]["@last_uuid"]

with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO competition_category (name) VALUES ('name 1')")
    cursor.execute("SELECT @last_uuid;")
    new_category1_id = cursor.fetchall()[0]["@last_uuid"]

with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO competition_category (name) VALUES ('name 2')")
    cursor.execute("SELECT @last_uuid;")
    new_category2_id = cursor.fetchall()[0]["@last_uuid"]

with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO category_group (category_id, group_id) VALUES ('{0}', '{1}')".format(new_category1_id, new_group1_id))

with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO category_group (category_id, group_id) VALUES ('{0}', '{1}')".format(new_category2_id, new_group1_id))

response = login_session.get(BACKEND_URL+"/groups/{0}/alldata".format(new_group1_id)).content.decode("utf-8")
to_compare = '{{"groups_ID_alldata":{{"competition_categories":["name 1","name 2"],"hacking_space":"space 1","id":"{0}","name":"name 1"}}}}\n'.format(new_group1_id)

if response == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("response: \n{0}".format(response))
    print("to_compare: \n{0}".format(to_compare))
    print("test failed: /groups/ID/alldata - positive test")
    index_of_string_difference(response, to_compare)
    test_count += 1

clean_all_tables()



### /groups/ID/update - positive test
with PyMySQL.cursor() as cursor:
    cursor.execute("INSERT INTO `group` (name, space, hack_submitted) VALUES ('name 1', 'space 1', 0)")
    cursor.execute("SELECT @last_uuid;")
    new_group1_id = cursor.fetchall()[0]["@last_uuid"]

request_body = {"name": "name 2", "hacking_space": "space 2", "hack_submitted": 1}
response = login_session.put(BACKEND_URL+"/groups/{0}/update".format(new_group1_id), json=request_body).content.decode("utf-8")

with PyMySQL.cursor() as cursor:
    cursor.execute("SELECT * FROM `group` WHERE group_id='{0}'".format(new_group1_id))
    query_result = str(cursor.fetchall())

to_compare = "[{{'group_id': '{0}', 'name': 'name 2', 'space': 'space 2', 'hack_submitted': 1}}]".format(new_group1_id)

if query_result == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("response: \n{0}".format(query_result))
    print("to_compare: \n{0}".format(to_compare))
    print("test failed: /groups/ID/update - positive test")
    index_of_string_difference(query_result, to_compare)
    test_count += 1

clean_all_tables()



### /groups/create - positive test
request_body = {"name": "name 1", "hacking_space": "space 1", "hack_submitted": 0}
response = json.loads(login_session.post(BACKEND_URL+"/groups/create", json=request_body).content.decode("utf-8"))

with PyMySQL.cursor() as cursor:
    cursor.execute("SELECT * FROM `group`;")
    query_result = str(cursor.fetchall())

to_compare = "[{{'group_id': '{0}', 'name': 'name 1', 'space': 'space 1', 'hack_submitted': 0}}]".format(response["group_id"])

if query_result == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("response: \n{0}".format(query_result))
    print("to_compare: \n{0}".format(to_compare))
    print("test failed: /groups/create - positive test")
    index_of_string_difference(query_result, to_compare)
    test_count += 1

clean_all_tables()



### /loans/ID/loan/ID - positive test
query = "INSERT INTO `group` (name, space) VALUES ('group name 1', 'space 1');"
with PyMySQL.cursor() as cursor:
    cursor.execute(query)
    cursor.execute("SELECT @last_uuid;")
    new_group_id = cursor.fetchall()[0]["@last_uuid"]

query = "INSERT INTO `tool` (loaned, name, description, latest_loan) VALUES (0, 'tool name 1', 'tool description 1', null);"
with PyMySQL.cursor() as cursor:
    cursor.execute(query)
    cursor.execute("SELECT @last_uuid;")
    new_tool_id = cursor.fetchall()[0]["@last_uuid"]

response = login_session.post(BACKEND_URL+"/loans/{0}/loan/{1}".format(new_group_id, new_tool_id)).content.decode("utf-8")

query = "SELECT loan_id FROM loan WHERE loan_to_group_id='{0}' AND tool_id='{1}'".format(new_group_id, new_tool_id)
with PyMySQL.cursor() as cursor:
    cursor.execute(query)
    query_result_loan_id = cursor.fetchall()

if query_result_loan_id == []:
    print("test failed: /loans/ID/loan/ID - positive test")
    index_of_string_difference(query_result, to_compare)
    test_count += 1
else:
    query = "SELECT latest_loan FROM tool WHERE tool_id='{0}'".format(new_tool_id)
    with PyMySQL.cursor() as cursor:
        cursor.execute(query)
        query_result = cursor.fetchall()
    
    if query_result[0]["latest_loan"] == query_result_loan_id[0]["loan_id"]:
        pass_count += 1
        test_count += 1
    else:
        print("response: \n{0}".format(query_result))
        print("to_compare: \n{0}".format(to_compare))
        print("test failed: /loans/ID/loan/ID - positive test")
        index_of_string_difference(query_result, to_compare)
        test_count += 1

clean_all_tables()



### /loans/ID/loan/ID - negative test - tool has already been loaned out
query = "INSERT INTO `tool` (loaned, name, description, latest_loan) VALUES (1, 'tool name 1', 'tool description 1', '1');"
with PyMySQL.cursor() as cursor:
    cursor.execute(query)
    cursor.execute("SELECT @last_uuid;")
    new_tool_id = cursor.fetchall()[0]["@last_uuid"]

response = login_session.post(BACKEND_URL+"/loans/{0}/loan/{1}".format("1", new_tool_id)).content.decode("utf-8")
to_compare = '{"error":"tool has already been loaned out"}\n'

if response == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("response: \n{0}".format(response))
    print("to_compare: \n{0}".format(to_compare))
    print("test failed: /loans/ID/loan/ID - negative test - tool has already been loaned out")
    index_of_string_difference(response, to_compare)
    test_count += 1

clean_all_tables()



### /loans/return/ID - positive test
query = "INSERT INTO `tool` (loaned, name, description, latest_loan) VALUES (1, 'tool name 1', 'tool description 1', '1');"
with PyMySQL.cursor() as cursor:
    cursor.execute(query)
    cursor.execute("SELECT @last_uuid;")
    new_tool_id = cursor.fetchall()[0]["@last_uuid"]

response = login_session.put(BACKEND_URL+"/loans/return/{0}".format(new_tool_id)).content.decode("utf-8")

query = "SELECT loaned FROM tool WHERE tool_id='{0}'".format(new_tool_id)
with PyMySQL.cursor() as cursor:
    cursor.execute(query)
    query_result = str(cursor.fetchall())

to_compare = "[{'loaned': 0}]"

if query_result == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("response: \n{0}".format(query_result))
    print("to_compare: \n{0}".format(to_compare))
    print("test failed: /loans/return/ID - positive test")
    index_of_string_difference(query_result, to_compare)
    test_count += 1

clean_all_tables()



### /groups/ID/submit - positive test
query = "INSERT INTO `group` (name, space, hack_submitted) VALUES ('name 1', 'space 1', 0)"
with PyMySQL.cursor() as cursor:
    cursor.execute(query)
    cursor.execute("SELECT @last_uuid;")
    new_group_id = cursor.fetchall()[0]["@last_uuid"]

response = login_session.put(BACKEND_URL+"/groups/{0}/submit".format(new_group_id)).content.decode("utf-8")

query = "SELECT hack_submitted FROM `group` WHERE group_id='{0}'".format(new_group_id)
with PyMySQL.cursor() as cursor:
    cursor.execute(query)
    query_result = str(cursor.fetchall())

to_compare = "[{'hack_submitted': 1}]"

if query_result == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("response: \n{0}".format(query_result))
    print("to_compare: \n{0}".format(to_compare))
    print("test failed: /groups/ID/submit - positive test")
    index_of_string_difference(query_result, to_compare)
    test_count += 1

clean_all_tables()



### /groups/ID/unsubmit - positive test
query = "INSERT INTO `group` (name, space, hack_submitted) VALUES ('name 1', 'space 1', 1)"
with PyMySQL.cursor() as cursor:
    cursor.execute(query)
    cursor.execute("SELECT @last_uuid;")
    new_group_id = cursor.fetchall()[0]["@last_uuid"]

response = login_session.put(BACKEND_URL+"/groups/{0}/unsubmit".format(new_group_id)).content.decode("utf-8")

query = "SELECT hack_submitted FROM `group` WHERE group_id='{0}'".format(new_group_id)
with PyMySQL.cursor() as cursor:
    cursor.execute(query)
    query_result = str(cursor.fetchall())

to_compare = "[{'hack_submitted': 0}]"

if query_result == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("response: \n{0}".format(query_result))
    print("to_compare: \n{0}".format(to_compare))
    print("test failed: /groups/ID/unsubmit - positive test")
    index_of_string_difference(query_result, to_compare)
    test_count += 1

clean_all_tables()



### /consumables/ID/take/ID/COUNT - positive test
query = "INSERT INTO consumable (name, description, stock_qty, total_qty, quota_per_group) VALUES ('consumable name 1', 'consumable description 1', 6, 10, 3);"
with PyMySQL.cursor() as cursor:
    cursor.execute(query)
    cursor.execute("SELECT @last_uuid;")
    new_consumable_id = cursor.fetchall()[0]["@last_uuid"]

query = "INSERT INTO `group` (name, space) VALUES ('group name 1', 'group space 1');"
with PyMySQL.cursor() as cursor:
    cursor.execute(query)
    cursor.execute("SELECT @last_uuid;")
    new_group_id = cursor.fetchall()[0]["@last_uuid"]

query = "INSERT INTO consumable_group (group_id, consumable_id, qty) VALUES ('{0}', '{1}', 3);".format(new_group_id, new_consumable_id)
with PyMySQL.cursor() as cursor:
    cursor.execute(query)

response = login_session.put(BACKEND_URL+"/consumables/{0}/take/{1}/{2}".format(new_group_id, new_consumable_id, 2), json=request_body).content.decode("utf-8")

query = "SELECT qty FROM consumable_group WHERE group_id='{0}' AND consumable_id='{1}'".format(new_group_id, new_consumable_id)
with PyMySQL.cursor() as cursor:
    cursor.execute(query)
    query_result = str(cursor.fetchall())

to_compare = "[{'qty': 1}]"

if query_result == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("response: \n{0}".format(query_result))
    print("to_compare: \n{0}".format(to_compare))
    print("/consumables/ID/take/ID/COUNT - positive test")
    index_of_string_difference(query_result, to_compare)
    test_count += 1

clean_all_tables()



### /consumables/ID/return/ID/COUNT - positive test
query = "INSERT INTO consumable (name, description, stock_qty, total_qty, quota_per_group) VALUES ('consumable name 1', 'consumable description 1', 6, 10, 3);"
with PyMySQL.cursor() as cursor:
    cursor.execute(query)
    cursor.execute("SELECT @last_uuid;")
    new_consumable_id = cursor.fetchall()[0]["@last_uuid"]

query = "INSERT INTO `group` (name, space) VALUES ('group name 1', 'group space 1');"
with PyMySQL.cursor() as cursor:
    cursor.execute(query)
    cursor.execute("SELECT @last_uuid;")
    new_group_id = cursor.fetchall()[0]["@last_uuid"]

query = "INSERT INTO consumable_group (group_id, consumable_id, qty) VALUES ('{0}', '{1}', 1);".format(new_group_id, new_consumable_id)
with PyMySQL.cursor() as cursor:
    cursor.execute(query)

response = login_session.put(BACKEND_URL+"/consumables/{0}/return/{1}/{2}".format(new_group_id, new_consumable_id, 2), json=request_body).content.decode("utf-8")

query = "SELECT qty FROM consumable_group WHERE group_id='{0}' AND consumable_id='{1}'".format(new_group_id, new_consumable_id)
with PyMySQL.cursor() as cursor:
    cursor.execute(query)
    query_result = str(cursor.fetchall())

to_compare = "[{'qty': 3}]"

if query_result == to_compare:
    pass_count += 1
    test_count += 1
else:
    print("response: \n{0}".format(query_result))
    print("to_compare: \n{0}".format(to_compare))
    print("/consumables/ID/return/ID/COUNT - positive test")
    index_of_string_difference(query_result, to_compare)
    test_count += 1

clean_all_tables()





remove_test_cred()
print("{0}/{1} test cases passed.".format(pass_count, test_count))
