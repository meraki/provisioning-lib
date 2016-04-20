import copy
import pytest
import meraki_admins

with open('key', 'r') as api_key:
    TEST_CONNECTOR = meraki_admins.DashboardAdmins("524681",
                                                   api_key.read().strip())

VALID_USERS = [
    {"name": "test 1", "email": "test1@test.foo", "orgAccess": "read-only"},
    {"name": "test 2", "email": "test2@test.foo", "orgAccess": "none",
     "tags": [{"tag": "test tag", "access": "read-only"}]},
    {"name": "test 3", "email": "test3@test.foo", "orgAccess": "none",
     "networks": [{"access": "read-only", "id": "N_629378047925034734"}]},
    {"name": "test 4", "email": "test4@test.foo", "orgAccess": "none",
     "networks": [{"access": "monitor-only", "id": "N_629378047925034734"}],
     "tags": [{"tag": "another one", "access":"guest-ambassador"},
              {"tag": "last try", "access":"full"}]}
    ]

VALID_UPDATES = [
    {"orgAccess": "full", "admin_id": VALID_USERS[0]["email"]},
    {"name": "test 2 changed", "admin_id": VALID_USERS[1]["email"]},
    {"networks": [{"access": "monitor-only", "id":"N_629378047925035587"}],
     "admin_id": VALID_USERS[2]["email"]},
    {"tags": [{"tag": "updated", "access": "guest-ambassador"}],
     "admin_id": VALID_USERS[3]["email"]}
    ]

def __pop_untested(user):
    """Dashboard returns an empty list for networks and tags if they're not
       specified, so pop them along with unique user ID string."""

    for key in user.keys():
        if (key == "id" or isinstance(user[key], list) and
                len(user[key]) == 0):
            user.pop(key)
    return user

def test_add_valid():
    """Testing all valid add conditions for users. Assert Dashboard returns HTTP
       201 per the API documentation for adding users, and that all submitted
       user parameters are returned unmodified."""

    for user in VALID_USERS:
        test_request = TEST_CONNECTOR.add_admin(**user)
        posted_user = test_request.json()

        posted_user = __pop_untested(posted_user)

        check_user = user.items()
        check_user.sort()
        check_posted = posted_user.items()
        check_posted.sort()
        assert check_user == check_posted and test_request.status_code == 201


def test_update_valid():
    """Testing all valid modifications for existing users. Assert Dashboard
       returns HTTP 200 and that only submitted parameters are returned
       modified."""

    original_users = copy.deepcopy(VALID_USERS)
    for user in VALID_UPDATES:
        test_request = TEST_CONNECTOR.update_admin(**user)
        updated_user = test_request.json()

        updated_user = __pop_untested(updated_user)

        check_user = user.items()
        check_user.sort()
        check_posted = updated_user.items()
        check_posted.sort()

        # Remove modfied values from the posted sample
        # This does not work yet
        for key in user.keys():
            pass



def test_del_valid():
    """Testing deleting existing users. Assert Dashboard returns HTTP 204, and
       that they're no longer contained in the user list post-removal."""

    for user in VALID_USERS:
        test_delete = TEST_CONNECTOR.del_admin(user["email"])
        assert test_delete.status_code == 204

if __name__ == '__main__':
    test_add_valid()
