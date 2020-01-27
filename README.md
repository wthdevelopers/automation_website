# WTHack-Automation website v2.0

A website that automates some workflows required to plan/execute WTHack 2020


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

### Version history
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
