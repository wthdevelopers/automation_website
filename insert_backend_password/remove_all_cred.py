import pymysql as pms
import sys, os

dirname = os.path.dirname(__file__)
sys.path.append(os.path.join(dirname, "../backend"))
from config import Production, RemoteTest

database_name = input("Please input 'Production' or 'RemoteTest' to select the database to remove all credentials from: ")

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


query = "DELETE FROM `credentials`"

with conn.cursor() as cursor:
    cursor.execute(query)

print("All existing credentials deleted")

