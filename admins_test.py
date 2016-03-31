import pytest
import meraki_admins

test_connector = meraki_admins.DashboardAdmins()


def test_add_valid():
	valid_users = [
					{"name": "test 1", "email": "test1@test.lol",
					 "orgAccess": "read-only"}]
	for user in valid_users:
		test_request = test_connector.add_admin(user["name"], user["email"],
										 	 	user["orgAccess"])
		user_data = test_request.json()
		unhashables = {}

		for key in user_data.keys():
			if isinstance(user_data[key], list):
				unhashables[key] = user_data[key]
				user_data.pop(key)

		assert set(user.items()).issubset(set(user_data.items())) is True