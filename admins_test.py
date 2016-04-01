import pytest
import meraki_admins

with open('key', 'r') as api_key:
    TEST_CONNECTOR = meraki_admins.DashboardAdmins("524681",
                                                   api_key.read().strip())


def test_add_valid():
    """Testing all valid add conditions for users."""

    valid_users = [
        {"name": "test 1", "email": "test1@test.lol", "orgAccess": "read-only"},
        {"name": "test 2", "email": "test2@test.lol", "orgAccess": "none",
         "tags": [{"tag": "test tag", "access": "read-only"}]},
        {"name": "test 3", "email": "test3@test.lol", "orgAccess": "none",
         "networks": [{"access": "read-only", "id": "N_629378047925034734"}]}
        ]
    for user in valid_users:
        test_request = TEST_CONNECTOR.add_admin(**user)
        posted_user = test_request.json()
        user_unhashables = {}
        posted_unhashables = {}


        for key in posted_user.keys():
            if isinstance(posted_user[key], list):
                posted_unhashables[key] = posted_user[key]
                posted_user.pop(key)

                if key in user.keys():
                    user_unhashables[key] = user[key]
                    user.pop(key)

        assert (test_request.status_code == 201 and
                set(user.items()).issubset(set(posted_user.items())) is True)

if __name__ == '__main__':
    test_add_valid()
