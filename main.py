import os
import sys
from guest import get_guests, format_guest_info
from access_control import get_created_ac_users, create_groups_add_users

if __name__ == '__main__':

    # All three of these variables will need to be changed depending on your setup
    # This will match the name of the guest type that you are looking for in Command
    GUEST_TYPE = os.environ['GUEST_TYPE']
    # This is the site-id for the guest site the guests will be checking into
    GUEST_SITE_ID = os.environ['GUEST_SITE_ID']
    # Your API key will need to be made as an environment variable
    API_KEY = os.environ['VERKADA_API_KEY']
    # The name of the group made in AC that will have the access level tied to it
    AC_GROUP_ID = os.environ['AC_GROUP_ID']

    # Gets full list of guests and sorts for guests of particular type
    guest_list = get_guests(API_KEY, GUEST_SITE_ID)
    guests_of_given_type = format_guest_info(guest_list, GUEST_TYPE)

    # Will end program if no guests of particular type are found
    if not guests_of_given_type:
        print(f"No new {GUEST_TYPE}'s")
        sys.exit()
    else:
        print(f"{GUEST_TYPE}'s: {guests_of_given_type}")

    # Gets the ac users information for the newly created users
    ac_users_info = get_created_ac_users(API_KEY, guests_of_given_type)

    # Creates groups for each address found and
    create_groups_add_users(API_KEY, ac_users_info, AC_GROUP_ID)
