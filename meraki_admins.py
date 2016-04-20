import requests

BASE_URL = "https://dashboard.meraki.com/api/v0"
API_HEADER = "X-Cisco-Meraki-API-Key"
JSON_KEY = "Content-Type"
JSON_VAL = "application/json"


def get_data(headers, level="", request_string="", url_id="", ext_url=""):
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
            ext_url: an externally formatted URL; supersedes all other
                parameters if specified

        Returns:
            A requests.get object containing, among other things, the HTTP
            HTTP return code of the request, and the returned data.
    """
# TODO (Alex): Docstring needs some work here to build-out what different
# request strings indicate, and will need to work on adding exceptions.

    if ext_url:
        data = requests.get(ext_url, headers=headers)
    else:
        url = "%s/%s/%s/%s/" % (BASE_URL.strip("/"), level.strip("/"),
                                url_id.strip("/"), request_string.strip("/"))
        data = requests.get(url, headers=headers)
    return data

class Error(Exception):
    """Base module exception."""
    pass

class InvalidOrgPermissions(Error):
    """Thrown when invalid Org-level permissions are supplied."""
    def __init__(self, provided=None, valid=None):
        self.provided = provided
        self.valid = valid
        self.default = "Org Permissions must be FULL, READ-ONLY, or NONE"

    def __str__(self):
        return repr(self.default)

class InvalidNetTagPermissions(Error):
    """Thrown when invalid Network or Tag permissions are supplied."""
    pass

class NullPermissionError(Error):
    """Thrown when no permissionsare supplied."""
    def __init__(self):
        self.default = "No Org or Tag/Network level permissions supplied."

    def __str__(self):
        return repr(self.default)

class FormatError(Error):
    """Thrown when imprperly formatted data received."""
    pass

class DashboardAdmins(object):
    """ All methods and handlers to define, modify, or remove an
        admin from a given Dashboard account.
    """
    def __init__(self, org_id, api_key):
        self.url = "%s/organizations/%s/admins" % (BASE_URL, org_id)
        self.valid_tag_keys = {"tag", "access"}
        self.valid_access_vals = {"full", "read-only", "none"}
        self.valid_target_vals = self.valid_access_vals.union({"monitor-only",
                                                               "guest-ambassador"})

        self.headers = {API_HEADER: api_key}


    def __provided_access_valid(self, access):
        if (access not in self.valid_access_vals and
                access not in self.valid_target_vals):
            raise InvalidOrgPermissions(access, self.valid_access_vals)


    def __provided_tags_valid(self, tags):
        if not isinstance(tags, list):
            raise TypeError("Tags must be provided as a list of dictionaries.")

        for i in tags:
            if not isinstance(i, dict):
                raise TypeError("Tags must be provided as \
                                a list of dictionaries.")
            elif not self.valid_tag_keys.issuperset(i.keys()):
                raise FormatError("Error in tag format.")
            self.__provided_access_valid(i["access"])


    def __admin_exists(self, admin_id):
        check = get_data(ext_url=self.url, headers=self.headers)
        try:
            for admin in check.json():
                if admin["email"] == admin_id or admin["id"] == admin_id:
                    return admin
        except ValueError: # Ignore empty responses
            pass

        return None


    def add_admin(self, name, email, orgAccess, networks=None, tags=None):
        """ Define a new org-level Admin account on Dashboard under
            Organization -> Administrators.
            Args:
                name: Name of the new admin.
                email: Email of the new admin.
                orgAccess: Their access level; valid values are full,
                read-only, or none (for tag or network-level admins)
                networks: A list of dictionaries formatted as
                [{id: network-id, access: access-level}]; networks must be
                prexisting on Dashboard.
                tags: A list of dictionaries formatted as
                [{tag:tag-name}, {access:access-level}]; tags don't need to be
                prexisting on Dashboard.
            Returns:
                new_admin: a request object of the new admin's values
                as specified by the passed arguments and the HTTP
                return code for it, or None if the user already exists
        """

        admin = {"name": name, "email": email, "orgAccess": orgAccess}
        self.__provided_access_valid(orgAccess)
        if orgAccess.lower() == "none" and not tags and not networks:
            raise NullPermissionError()

        if tags:
            self.__provided_tags_valid(tags)
            admin["tags"] = tags
        if networks:
            admin["networks"] = networks # still deciding how this is going to
                                         # be validated

        new_admin = requests.post(self.url, json=admin, headers=self.headers)

        return new_admin


    def update_admin(self, admin_id, name=None, orgAccess=None, networks=None,
                     tags=None):
        """Update an existing admin's permissions or access.

        Dashboard ignores null or None values in spite of what it returns, and
        will not modify anything based on null parameters.

        Args:
            admin_id: A user ID string or email address.
            to_update: a dict of the fields to be updated; valid keys are
            orgAccess, name, tags, and network.
        Returns:
            updated: The request object of the updated admin, or None if the
            passed admin ID doesn't exist.
        """

        exists = self.__admin_exists(admin_id)
        if not exists:
            return None
        elif not admin_id.isdigit():
            admin_id = exists["id"]

        to_update = {"id": admin_id, "orgAccess": orgAccess, "name": name}
        update_url = self.url+"/"+admin_id

        if tags:
            self.__provided_tags_valid(tags)
            to_update["tags"] = tags

        if orgAccess:
            try:
                self.__provided_access_valid(orgAccess)
            except InvalidOrgPermissions as err:
                print "ERROR: Invalid permissions for user %s \nPROVIDED: %s \
                \nEXPECTED: %s" % (admin_id, err.provided, err.valid)

        if networks:
            to_update["networks"] = networks

        updated = requests.put(url=update_url, json=to_update,
                               headers=self.headers)
        return updated


    def del_admin(self, admin_id):
        """ Delete a specified admin account.
            Args:
                admin_id: ID string or email of the admin to be deleted.
            Returns:
                deleted: The request object of the deleted admin, or None if the
                passed admin ID doesn't exist.
        """

        exists = self.__admin_exists(admin_id)
        if not exists:
            return None
        elif not admin_id.isdigit():
            admin_id = exists["id"]

        url = self.url+"/"+admin_id

        return requests.delete(url, headers=self.headers)


