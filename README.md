# Note about the structure of this code
Folder structure looks generally like this:

root
- /backend
--- /app
------ /modules
--- /venvBackend
- /frontend

At the top most layer, we separate frontend and backend (each will be running individual apps which will connect to each other using ports). 

In the next layer, it contains:
- setup scripts (Dockerfile, requirements.txt, shell scripts)
- the folder used to store the virtual environment to use during development (venvBackend)
- configuration information required to connect to plugins like MySQL (config.py)
- the folder that contains our backend app (app)
- and the entry point of our flask app (wsgi.py)

In the next layer, it contains:
- init file that creates the app (using a flask app factory) to represent our entire app
- the folder to contain the logic of each endpoint (modules)


References
Flask app's app factory:
https://hackersandslackers.com/demystifying-flask-application-factory/

Flask app's blueprints (to use in conjunction with app factory):
https://flask.palletsprojects.com/en/1.1.x/blueprints/#blueprints
