# WTHack-Automation website v1.0

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
- 1.0
  - Change backend's /functions/upcoming_events to display upcoming events for participants instead of the upcoming duty roster activities for ocomm members
  - Change backend's /functions/upcoming_events to display upcoming events for participants instead of the upcoming duty roster activities for ocomm members
  - Change operations on the resource "events"  to be on events for participants instead of the upcoming duty roster activities for ocomm members
  - Removed /ocomm/get_all
  - Update keys of response json to correspond to the name of the endpoint
- 2.0
  - endpoint "functions/find_participants" to be removed
  - NEW endpoint participants/get_all
    - returns id, name, registered status
  - NEW endpoint consumables/get_all
    - returns id, name, remaining count, quota per group
  - NEW endpoint groups/get_all
    - returns id, name, hacking space
  - NEW endpoint participants/<participant UID>/alldata
    - returns all column data
  - change "participants/register" to "participants/<participant UID>/register"
    - add checks before returning success message, otherwise return errors
  - NEW endpoint "participants/<participant UID>/deregister"
  - NEW endpoint "participants/<participant UID>/update"
    - add checks before returning success message, otherwise return errors
  - NEW endpoint "groups/<group UID>/alldata"
    - returns all column data
  - NEW endpoint "groups/<group UID>/update"
    - add checks before returning success message, otherwise return errors
  - NEW endpoint "groups/<group UID>/submit"
    - add checks before returning success message, otherwise return errors
    - checks before submitting a hack on Devpost
  - NEW endpoint "groups/<group UID>/unsubmit"
    - checks before unsubmitting a hack on Devpost
  - NEW endpoint "participants/<participant UID>/group"
    - returns whether the participant exist, and whether it belongs in an existing group already
  - NEW endpoint "groups/create"
    - add checks before returning success message, otherwise return errors
    - creates new groups
  - NEW endpoint "consumables/<group UID>/take/<consumable UID>/<count>"
    - add checks before returning success message, otherwise return errors
    - check if group is allowed to have this consumable at this amount
  - NEW endpoint "consumables/<group UID>/return/<consumable UID>/<count>"
  - Remove all event endpoints, and function/upcoming_events (seds)
