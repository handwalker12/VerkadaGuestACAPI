import requests
from checks import (
    name_splitter,
    payload_creator,
    check_for_server_error,
    check_user_previously_created,
    add_user_to_created_users,
)
import json


def add_user_to_group(api_key, user_id, group_id) -> json:
    """Adds user to group by given id's"""
    print("Attempting to add user to group")
    url = "https://api.verkada.com/access/v1/access_groups/group/user"

    params = {"group_id": group_id}

    payload = {"user_id": user_id}

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": api_key,
    }

    response = check_for_server_error(
        lambda: requests.put(url=url, headers=headers, json=payload, params=params)
    )

    return response.json()


def create_group(api_key, group_name) -> json:
    """Creates a new ac group with the provided name."""
    print("Creating new group")
    url = "https://api.verkada.com/access/v1/access_groups/group"

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": api_key,
    }

    payload = {"name": group_name}

    response = check_for_server_error(
        lambda: requests.post(url=url, headers=headers, json=payload)
    )

    return response.json()


def create_groups_add_users(api_key, ac_user_list, existing_ac_group_id) -> None:
    """Given a list of ac users, will run create_group_if_not_exists()
    and then add that user to the newly created group
    """
    for ac_user in ac_user_list:
        group_id = create_group_if_not_exists(api_key, ac_user["address"])
        user_add_to_group_response = add_user_to_group(
            api_key, ac_user["user_id"], group_id
        )
        print(f"Server Response: {user_add_to_group_response}")
        user_add_to_group_response = add_user_to_group(
            api_key, ac_user["user_id"], existing_ac_group_id
        )
        print(f"Server Response: {user_add_to_group_response}")


def create_group_if_not_exists(api_key, new_group_name) -> str:
    """Checks if the ac group exists and will create it if not using the provided group name."""
    group_list = get_groups(api_key)

    for group in group_list["access_groups"]:
        if new_group_name in group["name"]:
            print(f"Group Already Exists\nGroup_ID: {group['group_id']}")
            return group["group_id"]

    response = create_group(api_key, new_group_name)
    print(f"Group Created!\nGroup_ID: {response['group_id']}")
    return response["group_id"]


def create_new_user(api_key, new_user) -> json:
    """Creates a new user using the user dict provided."""
    print("Creating new user")
    url = "https://api.verkada.com/core/v1/user"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": api_key,
    }

    payload = {
        "department": new_user["address"],
        "email": new_user["email"],
        "first_name": new_user["first_name"],
        "middle_name": new_user["middle_name"],
        "last_name": new_user["last_name"],
        "phone": new_user["phone"],
    }

    response = check_for_server_error(
        lambda: requests.post(url=url, headers=headers, json=payload)
    )
    return response.json()


def create_user_if_not_exists(api_key, new_user) -> dict:
    """Will check if the user already exists and creates them if not
    using the provided new user information and list of existing ac users.
    """
    user_list = get_access_users(api_key)
    for user in user_list:
        user_names = name_splitter(user["full_name"])

        # Checks if the user has been previously created by this script
        if check_user_previously_created(user["user_id"]):
            new_user["ac_exists"] = True
            new_user["user_id"] = user["user_id"]

            return new_user

        # Checks if the emails match
        if new_user["email"] == user["email"]:
            print(f"{new_user['email']} already exists, updating information")
            new_user["ac_exists"] = True
            new_user["user_id"] = user["user_id"]
            update_users_information(api_key, new_user["user_id"], new_user["address"])
            add_user_to_created_users(new_user["user_id"])

            return new_user

        # Checks if the full name is the same
        elif (
            new_user["first_name"] == user_names["first_name"]
            and new_user["middle_name"] == user_names["middle_name"]
            and new_user["last_name"] == user_names["last_name"]
        ):
            print(
                f"{new_user['first_name']} {new_user['last_name']} already exists, updating information"
            )
            new_user["ac_exists"] = True
            new_user["user_id"] = user["user_id"]
            update_users_information(api_key, new_user["user_id"], new_user["address"])
            add_user_to_created_users(new_user["user_id"])

            return new_user

    # Creates the new user, sends pass app invite, updates created_users.txt
    create_user_response = create_new_user(api_key, new_user)
    new_user["ac_exists"] = True
    new_user["user_id"] = create_user_response["user_id"]
    print(f"User Created!\nUser Info: {new_user}")
    send_pass_app_invite(api_key, new_user["user_id"])
    add_user_to_created_users(new_user["user_id"])

    return new_user


def get_access_users(api_key) -> list:
    """Gets all access control users."""
    url = "https://api.verkada.com/access/v1/access_users"
    headers = {"accept": "application/json", "x-api-key": api_key}

    response = check_for_server_error(lambda: requests.get(url=url, headers=headers))

    return response.json()["access_members"]


def get_all_user_info(api_key, user_id) -> json:
    """Gets all the information from an existing user."""
    url = "https://api.verkada.com/core/v1/user"

    params = {"user_id": user_id}

    headers = {"accept": "application/json", "x-api-key": api_key}

    response = check_for_server_error(
        lambda: requests.get(url=url, headers=headers, params=params)
    )

    return response.json()


def get_created_ac_users(api_key, new_users) -> list:
    """Given a list of new users to create, will run create_user_if_not_exists()
    for each and return the list of new users.
    """
    list_of_new_users = []

    for user in new_users:
        created_user_output = create_user_if_not_exists(api_key, user)
        list_of_new_users.append(created_user_output)

    return list_of_new_users


def get_groups(api_key) -> json:
    """Gets all AC groups."""
    url = "https://api.verkada.com/access/v1/access_groups"

    headers = {"accept": "application/json", "x-api-key": api_key}

    response = check_for_server_error(lambda: requests.get(url=url, headers=headers))

    return response.json()


def send_pass_app_invite(api_key, user_id) -> None:
    """Sends the Pass App invite to the given user_id."""
    print("Sending Pass App Invite")
    url = "https://api.verkada.com/access/v1/access_users/user/pass/invite"

    params = {"user_id": user_id}

    headers = {"accept": "application/json", "x-api-key": api_key}

    check_for_server_error(
        lambda: requests.post(url=url, headers=headers, params=params)
    )


def update_users_information(api_key, user_id, input_address) -> None:
    """Given a user_id and any additional params available in the body params of the Update User API call, will update
    the users information: https://apidocs.verkada.com/reference/putuserviewv1
    """
    url = "https://api.verkada.com/core/v1/user"

    params = {"user_id": user_id}

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": api_key,
    }

    user_info = get_all_user_info(api_key, user_id)
    payload = payload_creator(user_info, input_address)

    response = check_for_server_error(
        lambda: requests.put(url=url, headers=headers, json=payload, params=params)
    )

    print(f"Server Response: {response.json()}")
