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
     "admin_id": VALID_UPDATES[3]["email"]}
    ]

def test_add_valid():
    """Testing all valid add conditions for users. Assert Dashboard returns HTTP
        201 per the API documentation for adding users, and that all submitted
        user parameters are returned unmodified."""

    for user in VALID_USERS:
        test_request = TEST_CONNECTOR.add_admin(**user)
        posted_user = test_request.json()
        user_unhashables = {}
        posted_unhashables = {}


        for key in posted_user.keys():
            if isinstance(posted_user[key], list):
                posted_unhashables[key] = posted_user.pop(key)

                if key in user.keys():
                    user_unhashables[key] = user.pop(key)

        assert (test_request.status_code == 201 and
                set(user.items()).issubset(set(posted_user.items())) is True)

def test_del_valid():
    "Testing deleting existing users. Assert Dashboard returns 204."

    for user in VALID_USERS:
        test_delete = TEST_CONNECTOR.del_admin(user["email"])
        assert test_delete.status_code == 204

if __name__ == '__main__':
    test_add_valid()
