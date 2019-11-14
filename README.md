# Github conventions
### Brancing
backend/{feature_name}
or
frontend/{feature_name}

For those that are unfamiliar with Git, you can refer to existing tutorials like
https://git-scm.com/docs/gittutorial

Or just drop any of the seniors/myself (jun de) if you have any questions

### Commit messages
E.g.
You have added a funciton Y in /backend/a.py, and included descriptions of it in README.md, your commit message can look like this:
"Add function Y in /backend/a.py to {insert brief description}; Include description of function Y in README.md"

Be concise, hence the rough format: {action} -> {location} -> {purpose (not always needed)}


# About the structure of this code
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
