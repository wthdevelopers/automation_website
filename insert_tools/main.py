from openpyxl import load_workbook
import pymysql as pms

import sys, os
dirname = os.path.dirname(__file__)
sys.path.append(os.path.join(dirname, "../backend"))
from config import Production, RemoteTest

flask_env = os.environ.get("FLASK_ENV", "RemoteTest")
if flask_env == "Production":
    ENV = Production
elif flask_env == "RemoteTest":
    ENV = RemoteTest

connection = pms.connect(host=ENV.HOST,
                   user=ENV.USER,
                   password=ENV.PW,
                   db=ENV.DB_NAME)
connection.autocommit(True)

item_name_list = [
    "Arduino Starter Kit (with Sensors)",
    "Arduino Basic Kit",
    "ESP 32 Wifi and BT module",
    "DHT11 Temperature Sensor",
    "HC-SR04 Ultrasonic Sensor",
    "HC-SR501 PIR Sensor",
    "MPU-6050 3 Axis Gyro",
    "2 Axis XYZ Analog Joystick",
    "Small Microphone Sound Sensor"
]

item_details = {
    "Arduino Starter Kit (with Sensors)": {"id_prefix": "ASK_", "total_qty":18},
    "Arduino Basic Kit": {"id_prefix": "ABK_", "total_qty":20},
    "ESP 32 Wifi and BT module": {"id_prefix": "ESP_", "total_qty":20},
    "DHT11 Temperature Sensor": {"id_prefix": "DHT_", "total_qty":20},
    "HC-SR04 Ultrasonic Sensor": {"id_prefix": "UTS_", "total_qty":20},
    "HC-SR501 PIR Sensor": {"id_prefix": "PIR_", "total_qty":20},
    "MPU-6050 3 Axis Gyro": {"id_prefix": "GYR_", "total_qty":20},
    "2 Axis XYZ Analog Joystick": {"id_prefix": "JSK_", "total_qty":10},
    "Small Microphone Sound Sensor": {"id_prefix": "SS", "total_qty":10}
}

for each_item in item_name_list:
    for i in range(1, item_details[each_item]["total_qty"]+1):
        if each_item == "Small Microphone Sound Sensor":
            query = "INSERT INTO `tool` (tool_id, loaned, name) VALUES ('{0}{1}', 0, '{2}')".format(item_details[each_item]["id_prefix"], i, each_item)
        else:
            query = "INSERT INTO `tool` (tool_id, loaned, name) VALUES ('{0}{1:02}', 0, '{2}')".format(item_details[each_item]["id_prefix"], i, each_item)

        with connection.cursor() as cursor:
            cursor.execute(query)

print("doneski")

