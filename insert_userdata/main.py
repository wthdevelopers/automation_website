"""
Will continue after all endpoints are up
"""

import csv, os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, './data.csv')

index_dict = {
    "solo_or_team": 5,
    "solo": {
        "user_name": 7,
        "user_contact_number": 12,
        "user_email": 11,
        "user_DoB": 8,
        "user_gender": 9,
        "user_nationality": 10,
        "user_organisation": 16,
        "user_designation": 17,
        "user_dietary_pref": 18,
        "user_NoK_name": 28,
        "user_NoK_relationship": 29,
        "user_NoK_contact_number": 30,
        "user_shirt_size": 19,
        "user_previous_hackathons_attended": 20,
        "user_bringing_utensils": 21,
        "user_utensil_color": 23,
        "user_category_of_interest": 13,
        "user_technology_of_interest": 14,
        "user_utensil_name": 22,
        "user_skills": 15,
        "user_workshop_repurpose": 24,
        "user_workshop_fusion": 25,
        "user_workshop_ESP32": 26,
        "user_workshop_using": 27,
        "consent": 31
    },
    "team": {
        "user_name": 34,
        "user_contact_number": 39,
        "user_email": 38,
        "user_DoB": 35,
        "user_gender": 36,
        "user_nationality": 37,
        "user_organisation": 43,
        "user_designation": 44,
        "user_dietary_pref": 45,
        "user_NoK_name": 55,
        "user_NoK_relationship": 56,
        "user_NoK_contact_number": 57,
        "user_shirt_size": 46,
        "user_previous_hackathons_attended": 47,
        "user_bringing_utensils": 48,
        "user_utensil_color": 50,
        "user_category_of_interest": 40,
        "user_technology_of_interest": 41,
        "user_utensil_name": 49,
        "user_skills": 42,
        "user_workshop_repurpose": 51,
        "user_workshop_fusion": 52,
        "user_workshop_ESP32": 53,
        "user_workshop_using": 54,
        "group_name": 32,
        "group_have_full_team": 33
        "consent": 58
    }
}

with open(filename, "r") as read_file:
    spamreader = csv.reader(read_file, delimiter=',', quotechar='|')

    for row in spamreader:
        for each_row in enumerate(row):
            print(each_row)
        exit(0)