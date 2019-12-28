import flask
from flask import request, jsonify
import MySQLdb

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/user/get_all', methods=['GET'])
def get_all():
  try:
     db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="local-user",
                     passwd="password",
                     db='wthack')
     cursor = db.cursor()
     cursor.execute("SELECT * FROM user")     #show all users in user table
     rows = cursor.fetchall()
     resp = jsonify(rows)
     resp.status_code = 200
     return resp
  except Exception as e:
       print(e)
  finally:
       cursor.close() 
       db.close()

@app.route('/user/get_one/<uid>')
def get_one(uid):
  try:
     db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="local-user",            # your username
                     passwd="password",
                     db='wthack')
     cursor = db.cursor()
     cursor.execute("SELECT * FROM user WHERE uid=%s", (uid,))
     rows = cursor.fetchall()
     resp = jsonify(rows)
     resp.status_code = 200
     return resp
  except Exception as e:
       print(e)
  finally:
       cursor.close() 
       db.close()

@app.route('/user/get_all/name/<name>')
def get_all_name(name):
  try:
     db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="local-user",            # your username
                     passwd="password",
                     db='wthack')
     cursor = db.cursor()
     cursor.execute("SELECT * FROM user WHERE name=%s", (name,))
     rows = cursor.fetchall()
     resp = jsonify(rows)
     resp.status_code = 200
     return resp
  except Exception as e:
       print(e)
  finally:
       cursor.close() 
       db.close()

@app.route('/user/get_all/contact/<contact_number>')
def get_all_contact(contact_number):
  try:
     db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="local-user",            # your username
                     passwd="password",
                     db='wthack')
     cursor = db.cursor()
     cursor.execute("SELECT * FROM user WHERE contact_number=%s", (contact_number,))
     rows = cursor.fetchall()
     resp = jsonify(rows)
     resp.status_code = 200
     return resp
  except Exception as e:
       print(e)
  finally:
       cursor.close() 
       db.close()

@app.route('/user/get_all/email/<email>')
def get_all_email(email):
  try:
     db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="local-user",            # your username
                     passwd="password",
                     db='wthack')
     cursor = db.cursor() 
     cursor.execute("SELECT * FROM user WHERE email=%s", (email,))
     rows = cursor.fetchall()
     resp = jsonify(rows)
     resp.status_code = 200
     return resp
  except Exception as e:
       print(e)
  finally:
       cursor.close() 
       db.close()

@app.route('/user/get_all/gid/<gid>')
def get_all_gid(gid):
  try:
     db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="local-user",            # your username
                     passwd="password",
                     db='wthack')
     cursor = db.cursor() 
     cursor.execute("SELECT * FROM user WHERE gid=%s", (gid,))
     rows = cursor.fetchall()
     resp = jsonify(rows)
     resp.status_code = 200  
     return resp
  except Exception as e:
       print(e)
  finally:
       cursor.close() 
       db.close()


@app.route('/user/add_one', methods=['POST'])
def add_one_user():
  try:
     _json = request.json
     _name = _json['name']
     _contact_number = _json['contact_number']
     _email = _json['email']
     if isinstance(_json['gid'], basestring):
         _gid = _json['gid']
     else:
         _gid = 0   # will be 0 if its a single person and group name for group id
     _participating = 0  # assumed as not coming until comes for actual event

   # validate the received values
     if _name and _contact_number and _email and request.method == 'POST':

     # save edits
          sql = "INSERT INTO user(name, contact_number, email, gid, participating) VALUES(%s, %s, %s, %s, %s)" # Adds users information to user table
          data = (_name, _contact_number, _email, _gid, _participating)
          db = MySQLdb.connect(host="localhost",
                               user="local-user",
                               passwd="password",
                               db='wthack') 
          cursor = db.cursor()
          cursor.execute(sql, data)
          db.commit()
          resp = jsonify('User added successfully!')
          resp.status_code = 200
          return resp
     else:
        return not_found()
  except Exception as e:
       print(e)
  finally:
       cursor.close() 
       db.close()


@app.route('/user/update_one', methods=['POST'])
def update_one_user():
  try:
     _json = request.json
     _uid = _json['uid']    #Uses uid to find user that you want to update
     _name = _json['name']
     _contact_number = _json['contact_number']
     _email = _json['email'] 
     _gid = _json['gid']  # will be null if its a single person, group name for group id
     _participating = 0  # assumed as not coming until comes for actual event

   # validate the received values
     if _name and _contact_number and _email and request.method == 'POST':

     # save edits
          sql = "UPDATE user SET name=%s, contact_number=%s, email=%s, gid=%s, participating=%s WHERE uid=%s" #updates users information through uid
          data = (_name, _contact_number, _email, _gid, _participating, _uid)
          db = MySQLdb.connect(host="localhost",
                               user="local-user",
                               passwd="password",
                               db='wthack') 
          cursor = db.cursor()
          cursor.execute(sql, data)
          db.commit()
          resp = jsonify('User updated successfully!')
          resp.status_code = 200
          return resp
     else:
        return not_found()
  except Exception as e:
       print(e)
  finally:
     cursor.close()
     db.close()

@app.route('/user/delete_one/<uid>')
def delete_one_user(uid):
  try:
     db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                                user="local-user",            # your username
                                passwd="password",
                                db='wthack') 
     cursor = db.cursor() 
     cursor.execute("DELETE FROM user WHERE uid=%s", (uid,))
     db.commit()
     resp = jsonify('User deleted successfully!')
     resp.status_code = 200
     return resp
  except Exception as e:
      print(e)
  finally:
     cursor.close()
     db.close()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

#Run flask app
app.run(host='0.0.0.0')
