import json


def name_splitter(full_name) -> dict:
    """Will split up a users full name into the dedicated segments.
    Honestly I shouldn't have to make this function but the API gods dictate it!
    """
    first_name = full_name.split()[0]
    middle_name = ""
    last_name = ""

    try:
        last_name = full_name.split()[2]
    except IndexError:
        last_name = full_name.split()[1]
    else:
        middle_name = full_name.split()[1]
        last_name = full_name.split()[2]

    names = {
        "first_name": first_name,
        "middle_name": middle_name,
        "last_name": last_name
    }

    return names


def payload_creator(info, input_address='') -> dict:
    """Creates the payload for the update users API call in AC"""
    possible_keys = ["company_name", "department", "department_id", "email", "employee_type", "external_id",
                     "first_name", "last_name", "middle_name", "phone"]
    keys = []
    for key in info:
        if key in possible_keys:
            keys.append(key)

    payload = {key: value for key, value in info.items()}

    if input_address:
        payload['department'] = input_address

    return payload


def check_address(visit_info) -> str:
    """Checks to make sure that the user has provided an address.
    Probably don't need this but just keeping in case.
    """
    try:
        address = visit_info['open_ended_responses'][0]['response']
    except IndexError:
        address = ""
    else:
        address = visit_info['open_ended_responses'][0]['response']

    return address


def check_for_server_error(request) -> json:
    """Function used to run requests and retry in the event there is a server error or a rate limit.
    Will also terminate the program in the event there is an error thrown due to improper setup.
    """
    response = request()
    while int(str(response.status_code)[0]) == 5 or response.status_code == 429:
        print(response)
        response = request()

    if int(str(response.status_code)[0]) == 4 and int(str(response.status_code)[2]) != 0:
        raise Exception(f"{response}\nStopping, please verify your environment variables!")

    return response


def check_user_created(u_id) -> bool:
    """Checks to see if the user has already been created from a previous script run."""
    try:
        with open("created_users.txt", "x+") as f:
            for line in f:
                if line.strip('\n') == u_id:
                    print("User previously created")
                    return True

            f.write(f"{u_id}\n")
    except FileExistsError:
        with open("created_users.txt", "r+") as f:
            for line in f:
                if line.strip('\n') == u_id:
                    print("User previously created")
                    return True

            f.write(f"{u_id}\n")

    return False
