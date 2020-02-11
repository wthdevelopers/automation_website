# WTHack-Automation website v3.0
### About
Backend flask server that implement some workflows (that are previously manually done) required to plan/execute WTHack 2020

The server provides a set of APIs that allows organising members to:
- View and edit user information
- Records the registration of members and whether they've been given cash vouchers for meals
- View, create, and edit groups and their information
- Records whether the groups have returned loaned utensils or not, and whether they've submitted their hacks
- Records the loan statuses of all tools
- Creates new entries of loans/returns of exisiting tools
- User authentication before accessing such endpoints

Additional

User Stories for this project:
https://docs.google.com/spreadsheets/d/1JzmQu9a42cI74bXLm_B3bhEId0I011isfi3b1agZ-RU/edit?usp=sharing

Backend:
- Published documentation for the endpoints: 
  https://documenter.getpostman.com/view/6948672/SWLcdoi7?version=latest
- DB schema: 
  https://hackmd.io/@xr4gYmdtSQG8THeA2Ifi5Q/BJrqSVvJL/edit

Frontend:
- Project requirements:
  https://hackmd.io/@Pengwin/rJ6uPyigL
- Designs for the frontend: 
  https://www.figma.com/file/LEd18NNjUkfn9yDlok3U8g/OComm-Front-End?node-id=0%3A1

### Setup
1. Set up the MySQL server in an instance with a public IP address by running ```sudo ./backend/setup.sh``` in that instance.
2. Copy backend/config_template.py into backend/config.py
3. Replace the values of each attribute of the classes
  - USER - Username used to access the MySQL database. Default value is "remote".
  - PW - Password used to access the MySQL database. Set this to the password you provided when setting up the MySQL database. Default value is "password".
  - HOST - The public IP address where the MySQL database is set up.
  - DB_NAME - The name of the database in the MySQL server. Default value is "wthack_automation".
  - PW_SALT - The salt used to salt the password used for authentication. Default value is "salt"
4. Insert credentials for logging into the flask server with ```./insert_backend_password/add_cred.py```
5. Populate tables with your custom scripts, or the ones available (insert_tools/, insert_userdata/, insert_judge_score/)
6. Set up complete. To run backend server, edit FLASK_ENV in backend/run_app.sh to either "RemoveTest" or "Production" depending on the config values you'd like to use. Finally, run ```./backend/run_app.sh```

### Run tests
1. Assuming that set up has been complete up to step 4, run ```./backend/tests/run_app_test.sh```
2. In the same instance, activate the python virtual environment with ```source ./backend/venvBackend/bin/activate```
3. Set the username and password to what you've configured in backend/tests/run_backend_tests.py
4. Run ```python3 ./backend/tests/run_backend_tests.py```
5. To exit the virtual environment, run ```deactivate```

### Existing functions
1. /insert_judge_score reads csv files of scores and judge values and input into the MySQL server
2. /retrieve_group_category outputs group, competition_category, and category_group table values into separate csv files

### Version history
- 3.0
  - DONE NEW table - category_user
    - person can have multiple options, separate table make it easier for querying
  - DONE NEW table - _user_preference_technology_of_interest
    - person can have multiple options, separate table make it easier for querying
  - DONE NEW table - _user_preference_technology_of_interest_user
  - DONE NEW table - _user_preference_skills
    - person can have multiple options, separate table make it easier for querying
  - DONE NEW table - _user_preference_skills_user
  - DONE NEW table - _user_preference_stojo_utensils
    - person can have multiple options, separate table make it easier for querying
  - DONE NEW table - _user_preference_stojo_utensils_user
  - DONE NEW table - _user_preference_workshops
  - DONE NEW table - _user_preference_workshops_user
  - DONE Update columnes for db table 'User' to reflect new question replies
    - /participants/ID/alldata - update the fields that it will display
    - /participants/ID/update - update the fields that it can change
  - DONE EDIT endpoint participants/ID/alldata
    - update DoB to match iso format of datetime
  - DONE EDIT endpoint participants/ID/update
    - remove ability to change group_id, and registered
    - only include key-value pairs (in the body of the request to be sent to the endpoint) when you need to edit those columns
  - DONE NEW endpoint groups/ID/update_members
    - Updates the team members in a group. If group no longer has any team members, group is deleted.
    - Check that user inserted does not belong in another group
  - !!! REMOVED endpoint categories/get_all
    - Gets all categories name and ID
    - removed as updating user/group details can just input category name (i.e. no longer need category ID)
  - DONE NEW endpoint consumables/ID/update
    - updates columnes for consumables. if total qty updated, increase stock_qty accordingly
    - check that quota_per_group * number_of_groups <= total_qty
    - not allowed to update stock_qty
    - quota_per_group is updated before total_qty
  - DONE EDIT endpoint groups/ID/update
    - include the ability to change categories that a group is registered in
    - remove hack_submitted
    - ensure ID of category exist in categories table before meeting request
  - DONE add new table category_judge
  - DONE no consumables feature
    - REMOVE ENDPOINT /consumables/get_all
    - REMOVE ENDPOINT /consumables/ID/return/ID/COUNT
    - REMOVE ENDPOINT /consumables/ID/take/ID/COUNT
    - REMOVE ENDPOINT /consumables/ID/update
    - REMOVE TABLE consumable, consumable_group
  - DONE NEW ENDPOINT /tools/get_all
    - Retrieves all attributes of the particular tool
    - get tools we return tool_id cos the organisers need it
  - DONE add notes_filepath to db table score datatype TEXT to store the path where the judges' notes will be stored
  - DONE add given_cash attribute to db table user
  - DONE NEW ENDPOINT /particiapnts/ID/given_cash
    - add new column to note if user has been given vouchers for meals (one time thing)
    - Changes the value of the column given_cash of db table user to 1
  - DONE NEW ENDPOINT /participants/ID/ungiven_cash
    - Changes the value of the column given_cash of db table user to 0
  - DONE EDIT endpoint group/create 
    - add ability to register participants to the group
  - DONE EDIT endpoint participants/deregister
    - remove participants from group
  - DONE EDIT endpoint groups/ID/alldata
    - include user id and name of members in group
  - DONE NEW FEATURE Function required to populate tools
  - DONE Ensure that empty strings are returned for all null values
  - DONE Ensure that all string inputs into mysql queries are escaped
  - DONE ensure all updates only update column if its included in request body
  - DONE add new column to db table group utensils_returned: not null, default value 0
  - DONE NEW ENDPOINT /groups/ID/utensils_returned
    - changes the column value utensils_returned of db table group to 1
  - DONE NEW ENDPOINT /groups/ID/utensils_loaned
    - changes the column value utensils_returned of db table group to 0
  - EDIT endpoint /participants/get_all now returns given_cash
- 2.0
  - DONE endpoint "functions/find_participants" to be removed
  - DONE Remove all event endpoints, and function/upcoming_events (seds)
    - functions/upcoming_events
    - event/delay_multiple
    - event/add_one
    - event/edit_one
    - event/delete_one
  - DONE remove participant/get_one
  - DONE NEW endpoint participants/get_all
    - returns id, name, registered status
  - DONE NEW endpoint participants/<participant UID>/alldata
    - returns all column data
  - DONE change "participants/register" to "participants/<participant UID>/register"
    - add checks before returning success message, otherwise return errors
  - DONE NEW endpoint "participants/<participant UID>/deregister"
  - DONE NEW endpoint "participants/<participant UID>/update"
    - add checks before returning success message, otherwise return errors
  - DONE NEW endpoint "participants/<participant UID>/group"
    - returns whether the participant exist, and whether it belongs in an existing group already
  - DONE NEW endpoint consumables/get_all
    - returns id, name, remaining count, quota per group
  - DONE NEW endpoint groups/get_all
    - Returns id, name, hacking space of all groups
  - DONE NEW endpoint "groups/<group UID>/alldata"
    - returns all column data
  - DONE NEW endpoint "groups/<group UID>/update"
    - updates all column values of group
    - add checks before returning success message, otherwise return errors
  - DONE NEW endpoint "groups/create"
    - add checks before returning success message, otherwise return errors
    - creates new groups
  - DONE change "item_loans/get_all" to "loans/get_all"
  - DONE NEW endpoint "loans/<group UID>/loan/<tool UID>"
    - Loans a tool to a specific group
    - add checks before returning success message, otherwise return errors
  - DONE NEW endpoint "loans/return/<tool UID>"
    - Returns a tool from a specific group
  - DONE NEW endpoint "groups/<group UID>/submit"
    - Registers that the group has submitted a hack
    - add checks before returning success message, otherwise return errors
    - checks before submitting a hack on Devpost
  - DONE NEW endpoint "groups/<group UID>/unsubmit"
    - checks before unsubmitting a hack on Devpost
  - DONE NEW endpoint "consumables/<group UID>/take/<consumable UID>/<count>"
    - Allow a group to consume a certain amount of consumables
    - add checks before returning success message, otherwise return errors
    - check if group is allowed to have this consumable at this amount
  - DONE NEW endpoint "consumables/<group UID>/return/<consumable UID>/<count>"
    - Allow a group to return a certain amount of consumables
  - Added login functionality
    - /login and /logout done, all other endpoints now require you to log in to access the endpoint
    - scripts written in /insert_backend_password allows you to set username and password
- 1.0
  - Change backend's /functions/upcoming_events to display upcoming events for participants instead of the upcoming duty roster activities for ocomm members
  - Change backend's /functions/upcoming_events to display upcoming events for participants instead of the upcoming duty roster activities for ocomm members
  - Change operations on the resource "events"  to be on events for participants instead of the upcoming duty roster activities for ocomm members
  - Removed /ocomm/get_all
  - Update keys of response json to correspond to the name of the endpoint

### Misc
Credits: SolsticeDante
Drop me an issue for any queries.