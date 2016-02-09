import requests

# Hard-Coding my URL and API key for now is a stopgap

ORG_ID = "349652"
BASE_URL = "https://n123.meraki.com/api/v0"
API_KEY = "X-Cisco-Meraki-API-Key"
API_VAL = "07668885586832243df6aefbea2a7fc1afb5cc8e"
JSON_KEY = "Content-Type"
JSON_VAL = "application/json"
HEADERS = {API_KEY: API_VAL, JSON_KEY: JSON_VAL}


def get_data(level="", request_string="", url_id="", ext_url=""):
    """ Defines a base get request to the Meraki Dashboard.
        One can be built using this function, or a pre-formatted one can be
        passed in.
        Args:
            level: A string of which level of data to query from; current valid
                top-level request types are organizations or networks.
            request_string: String indicating type of data to be queried; some
                requests such as determining Org access for a given API key do
                not require one.
            url_id: String containing an Org or Network ID.
            ext_url: an externally formatted URL.

        Returns:
            A requests.get object containing, among other things, the HTTP
            HTTP return code of the request, and the returned data.
    """
# TODO (Alex): Docstring needs some work here to build-out what different
# request strings indicate, and will need to work on adding exceptions.

    if ext_url:
        data = requests.get(ext_url, headers=HEADERS)
    else:
        url = "%s/%s/%s/%s/" % (BASE_URL.strip("/"), level.strip("/"),
                                url_id.strip("/"), request_string.strip("/"))
        data = requests.get(url, headers=HEADERS)
    return data

class AdminRequests(object):
    """ All methods, exceptions, and handlers to define, modify, or remove a
        Dashboard admin account.
    """
    def __init__(self):
        self.url = "%s/organizations/%s/admins" % (BASE_URL, ORG_ID)
        self.valid_access_keys = set(["tag", "access"])
        self.valid_access_vals = set(["full", "read-only", "none"])

    def _provided_access_valid(self, access):
        if access not in self.valid_access_vals:
            # TODO (Alex): Raise proper exception
            print "Invalid access type specified!"

    def _provided_tags_valid(self, tags):
        if not isinstance(tags, list):
            # TODO (Alex): raise exception properly here
            print "tags must be provided in a list!"

        for i in tags:
            if (not isinstance(i, dict)
                    or not self.valid_access_keys.issuperset(i.keys())
                    or not i["access"] in self.valid_access_vals):
                # TODO (Alex): raise exception properly here too
                # conditionals may have to be split out for
                # more verbose handling
                print "Incorrect format specified for tags!"

    def _admin_exists(self, admin_id):
        check = get_data(ext_url=self.url)
        for admin in check.json():
            if admin_id in admin.values():
                return admin

        return None


    def change_admin(self, name, email, access, admin_id=None, tags=None):
        """ Define a new Admin account on Dashboard under
            Organization -> Administrators, or update the parameters of an
            existing one.
            Args:
                name: Name of the new admin.
                email: Email of the new admin.
                access: Their access level; currently only supports full
                    admins, read-only admins, or tag-based admins; not
                    network-level admins.
                admin_id: The ID string of an existing admin.
                tags: A list of dictionaries formatted as
                [{tag:tag-name}, {access:access-level}]; tags don't need to be
                prexisting on Dashboard.

            Returns:
                changed_admin: a request object of the new or modified
                admin's values as specified by the passed arguments and the HTTP
                return code for it.
        """

        self._provided_access_valid(access)
        admin_data = {"name": name, "email": email, "orgAccess": access}
        if tags:
            self._provided_tags_valid(tags)
            admin_data["tags"] = tags

        if admin_id:
            update_url = "%s/%s/" % (self.url, admin_id)
            changed_admin = requests.put(update_url, json=admin_data,
                                         headers=HEADERS)
        else:
            changed_admin = requests.post(self.url, json=admin_data,
                                          headers=HEADERS)

        # TODO (Alex): Right now this just returns regardless of whether
        # the request was successful or not; this will need defined handlers.
        return changed_admin

    def del_admins(self, admin_id, skip_confirm=True):
        """ Delete a specified admin account.
            Args:
                admin_id: ID string of the admin to be deleted.
                no_confirm: Bool to prompt for confirmation before request is
                    submitted.
            Returns:
                delete_attempt: A dictionary of the deleted admin's
                ID and whether the operation succeeded. If a specified ID is not
                found, return None in its place.
        """

        delete_attempt = {None: False}
        url = "%s/%s" % (self.url, admin_id)
        to_delete = self._admin_exists(admin_id)

        if not to_delete:
            print "No admin with ID %s; skipping." % admin_id
            return delete_attempt

        elif not skip_confirm:
            prompt = ("Confirm deletion of user %s (%s) from organization %s "
                      "(y/n): ") % (to_delete["name"], to_delete["email"],
                                    ORG_ID)
            confirm = raw_input(prompt)
            if confirm.lower() == "n" or confirm.lower() == "no":
                print "Cancelling delete request\n"
                return delete_attempt

        requests.delete(url, headers=HEADERS)
        delete_attempt[admin_id] = True
        return delete_attempt


