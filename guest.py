import requests
from datetime import datetime
import time
from checks import name_splitter, check_address, check_for_server_error


def format_guest_info(response, guest_type) -> list:
    """Gets all the guests of type provided that have checked in then,
    reformats and returns their information into a list of sets.
    """
    print(f"Getting {guest_type}'s")
    guests = response["visits"]
    home_owners_visit = [
        home_owner for home_owner in guests if home_owner["visit_type"] == guest_type
    ]
    home_owners_info = []
    for visit in home_owners_visit:
        check_in = visit["check_in_time"]
        visit_names = name_splitter(visit["guest"]["full_name"])
        first_name = visit_names["first_name"]
        middle_name = visit_names["middle_name"]
        last_name = visit_names["last_name"]
        email = visit["guest"]["email"]
        phone = visit["guest"]["phone_number"]
        address = check_address(visit)

        home_owner = {
            "user_id": "",
            "check_in": check_in,
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "address": address,
            "ac_exists": False,
        }

        home_owners_info.append(home_owner)

    return home_owners_info


def get_guests(api_key, site_id) -> dict:
    """Gets all guests that have checked in on the current day."""
    print("Retrieving visitor list")

    today = datetime.today()
    today_unix = round(
        time.mktime(datetime.combine(today, datetime.min.time()).timetuple())
    )
    now_unix = round(time.mktime(datetime.now().timetuple()))

    url = "https://api.verkada.com/guest/v1/visits"
    headers = {"accept": "application/json", "x-api-key": api_key}
    params = {
        "site_id": site_id,
        "start_time": today_unix,
        "end_time": now_unix,
    }

    request = check_for_server_error(
        lambda: requests.get(url=url, headers=headers, params=params)
    )
    guest_response = request.json()

    return guest_response


def get_latest_checkin(guests) -> dict:
    """Gets the latest check-in of guests that match the type provided at start.
    This most likely won't be needed but here just in case.
    """
    latest_time = 0
    latest_guest = {}

    for guest in guests:
        if guest["check_in"] > latest_time:
            latest_time = guest["check_in"]
            latest_guest = guest

    return latest_guest
