import sys, os, pymysql, requests, datetime
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


### INSERT GROUPS
insert_group1_query = "INSERT INTO `group` (name, space) VALUES ('name 1', 'space 1')"
insert_group2_query = "INSERT INTO `group` (name, space) VALUES ('name 2', 'space 2')"
insert_group3_query = "INSERT INTO `group` (name, space) VALUES ('name 3', 'space 3')"

with PyMySQL.cursor() as cursor:
    cursor.execute(insert_group1_query)
    cursor.execute("SELECT @last_uuid;")
    new_group1_id = cursor.fetchall()[0]["@last_uuid"]

with PyMySQL.cursor() as cursor:
    cursor.execute(insert_group2_query)
    cursor.execute("SELECT @last_uuid;")
    new_group2_id = cursor.fetchall()[0]["@last_uuid"]

with PyMySQL.cursor() as cursor:
    cursor.execute(insert_group3_query)
    cursor.execute("SELECT @last_uuid;")
    new_group3_id = cursor.fetchall()[0]["@last_uuid"]


### INSERT USERS
insert_user1_query = "INSERT INTO user (name, \
    contact_number, \
    email, \
    group_id, \
    registered, \
    DoB, \
    gender, \
    nationality, \
    organisation, \
    designation, \
    dietary_pref, \
    NoK_name, \
    NoK_relationship, \
    NoK_contact_number,\
    shirt_size, \
    previous_hackathons_attended, \
    bringing_utensils, \
    team_allocation_preference, \
    utensil_color) \
VALUES ('user 1', \
    '90000001', \
    'test1.email.com', \
    '{0}', \
    0, \
    '2020-01-01', \
    'Female', \
    'singapore', \
    'SUTD', \
    'software engineer', \
    'Halal', \
    'NoK name 1', \
    'Parent', \
    '90000001', \
    'XS', \
    '0', \
    'I have mine and I\\'ll bring it!', \
    'soloist', \
    'Coral')".format(new_group1_id)

insert_user2_query = "INSERT INTO user (name, \
    contact_number, \
    email, \
    group_id, \
    registered, \
    DoB, \
    gender, \
    nationality, \
    organisation, \
    designation, \
    dietary_pref, \
    NoK_name, \
    NoK_relationship, \
    NoK_contact_number,\
    shirt_size, \
    previous_hackathons_attended, \
    bringing_utensils, \
    team_allocation_preference, \
    utensil_color) \
VALUES ('user 2', \
    '90000002', \
    'test2.email.com', \
    '{0}', \
    0, \
    '2020-02-02', \
    'Female', \
    'singapore', \
    'SUTD', \
    'software engineer', \
    'Halal', \
    'NoK name 2', \
    'Parent', \
    '90000002', \
    'XS', \
    '0', \
    'I have mine and I\\'ll bring it!', \
    'soloist', \
    'Coral')".format(new_group1_id)

insert_user3_query = "INSERT INTO user (name, \
    contact_number, \
    email, \
    group_id, \
    registered, \
    DoB, \
    gender, \
    nationality, \
    organisation, \
    designation, \
    dietary_pref, \
    NoK_name, \
    NoK_relationship, \
    NoK_contact_number,\
    shirt_size, \
    previous_hackathons_attended, \
    bringing_utensils, \
    team_allocation_preference, \
    utensil_color) \
VALUES ('user 3', \
    '90000003', \
    'test3.email.com', \
    '{0}', \
    0, \
    '2020-03-03', \
    'Female', \
    'singapore', \
    'SUTD', \
    'software engineer', \
    'Halal', \
    'NoK name 3', \
    'Parent', \
    '90000003', \
    'XS', \
    '0', \
    'I have mine and I\\'ll bring it!', \
    'soloist', \
    'Coral')".format(new_group2_id)

insert_user4_query = "INSERT INTO user (name, \
    contact_number, \
    email, \
    group_id, \
    registered, \
    DoB, \
    gender, \
    nationality, \
    organisation, \
    designation, \
    dietary_pref, \
    NoK_name, \
    NoK_relationship, \
    NoK_contact_number,\
    shirt_size, \
    previous_hackathons_attended, \
    bringing_utensils, \
    team_allocation_preference, \
    utensil_color) \
VALUES ('user 4', \
    '90000004', \
    'test4.email.com', \
    '{0}', \
    0, \
    '2020-04-04', \
    'Female', \
    'singapore', \
    'SUTD', \
    'software engineer', \
    'Halal', \
    'NoK name 4', \
    'Parent', \
    '90000004', \
    'XS', \
    '0', \
    'I have mine and I\\'ll bring it!', \
    'soloist', \
    'Coral')".format(new_group3_id)

with PyMySQL.cursor() as cursor:
    cursor.execute(insert_user1_query)

with PyMySQL.cursor() as cursor:
    cursor.execute(insert_user2_query)

with PyMySQL.cursor() as cursor:
    cursor.execute(insert_user3_query)

print("done.")

# ### INSERT SKILLS
# with PyMySQL.cursor() as cursor:
#     cursor.execute("INSERT INTO _user_preference_skills (name) VALUES ('Software');")
#     cursor.execute("SELECT @last_uuid;")
#     new_skill1_id = cursor.fetchall()[0]["@last_uuid"]

# with PyMySQL.cursor() as cursor:
#     cursor.execute("INSERT INTO _user_preference_skills (name) VALUES ('Electronics');")
#     cursor.execute("SELECT @last_uuid;")
#     new_skill2_id = cursor.fetchall()[0]["@last_uuid"]

# with PyMySQL.cursor() as cursor:
#     cursor.execute("INSERT INTO _user_preference_skills (name) VALUES ('Mechanical Hardware');")
#     cursor.execute("SELECT @last_uuid;")
#     new_skill3_id = cursor.fetchall()[0]["@last_uuid"]

# with PyMySQL.cursor() as cursor:
#     cursor.execute("INSERT INTO _user_preference_skills (name) VALUES ('Design (graphics, video, etc.)');")
#     cursor.execute("SELECT @last_uuid;")
#     new_skill4_id = cursor.fetchall()[0]["@last_uuid"]

