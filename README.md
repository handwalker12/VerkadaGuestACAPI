# Guest Check-In Automation Program

This program will check all guest check-ins from the current day and create an access user with their address taken from a free response question and saved under the user's department. A group will also be created from this address and the user will be added to it. The user will also be added into a group that you had created in Command which will ultimately determine what they have access to.

This will automate processes where users are required to fill out information on a first sign-in, whether this is for onboarding or for filling out documents like waivers, before they are given access to certain areas.

## Setup Instructions

Please follow these setup instructions to get this script working:

1. Set the environment variables to the appropriate values listed below:
| Key              | Description                                                                                                                                                                     |
|------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `VERKADA_API_KEY` | **Purpose:** API key with read/write permissions.<br>**Note:** Assign this from your Command organization and store it securely.                                                  |
| `GUEST_SITE_ID`   | **Purpose:** Site ID for the guest site.<br>**Note:** This is used for guest users signing in from the iPad.                                                                      |
| `GUEST_TYPE`      | **Purpose:** Guest type configuration.<br>**Note:** Requires an open-ended response question for users to input their address.                                                     |
| `AC_GROUP_ID`     | **Purpose:** Access control group ID.<br>**Note:** Tied to an access level that grants users automatic access to specific doors.                                                     |
2. Do a test run on this script with a user who has signed into the iPad to verify that all relevant information has been generated.

## FAQ

1. **What does "Stopping, please verify your environment variables!" mean?**
    - If you receive an error code in the console with "Stopping, please verify your environment variables!", you have most likely input one of your variables incorrectly.
2. **Code stuck printing server errors**
    - If you get stuck running a particular section of code and there are continuous server error responses given, this is either because you have hit the rate limit for the API and you will need to reach out to support to have this increased. Or, this is caused by an internal server error and will usually resolve itself after a few seconds.
3. **How do I assign user credentials?**
    - Currently, this will send the user an invite for the pass app which they will need to install. There is no current way to assign credentials through the API. Hopefully, this changes and I will attempt to update the script when it is possible. You could technically do access codes but unless you have the new intercom or a keypad reader, it's not relevant.
4. **What is the created_users.txt?**
    - This is a txt file that holds all of the user_ids previously created by this script. Removing this created_users.txt file will increase runtime, slightly, so I recommend keeping it in.
