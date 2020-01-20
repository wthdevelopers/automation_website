import pymysql as pms
import sys, os, hashlib

dirname = os.path.dirname(__file__)
sys.path.append(os.path.join(dirname, "../backend"))
from config import Production, RemoteTest


database_name = input("Please input 'Production' or 'RemoteTest' to select the database to remove all credentials from: ")
username = input("Please input new username: ")
password = input("Please input new password: ")

if database_name == "Production":
    ENV = Production
elif database_name == "RemoteTest":
    ENV = RemoteTest
else:
    print("Invalid database name, exiting program")
    exit()

conn = pms.connect(host=ENV.HOST,
                   user=ENV.USER,
                   password=ENV.PW,
                   db=ENV.DB_NAME)
conn.autocommit(True)

salted_password = password + ENV.PW_SALT

hashed_pw = hashlib.sha256(bytes(salted_password, "utf-8")).hexdigest()
print("hashed_pw: {0}".format(hashed_pw))

query = "INSERT INTO `credentials` (username, password) VALUES ('{0}', '{1}')".format(username, hashed_pw)

with conn.cursor() as cursor:
    cursor.execute(query)

print("new credentials uploaded.")
