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

class InvalidAccess(Error):
    """Thrown when improper permissions are supplied."""
    def __init__(self, provided, valid):
        self.provided = provided
        self.valid = valid

class FormatError(Error):
    """Thrown when imprperly formatted data received."""
    pass

class AdminRequests(object):
    """ All methods and handlers to define, modify, or remove a
        Dashboard admin account.
    """
    def __init__(self, org_id, api_key):
        self.url = "%s/organizations/%s/admins" % (BASE_URL, org_id)
        self.valid_access_keys = {"tag", "access"}
        self.valid_org_access_vals = {"full", "read-only", "none"}
        self.valid_net_access_vals = set.union(self.valid_org_access_vals,
                                               {"monitor-only",
                                                "guest-ambassador"})

        self.headers = {API_HEADER: api_key}


    def _provided_access_valid(self, access):
        if access not in self.valid_org_access_vals:
            raise InvalidAccess(access, self.valid_org_access_vals)


    def _provided_tags_valid(self, tags):
        if not isinstance(tags, list):
            raise TypeError("Tags must be provided as a list of dictionaries.")

        for i in tags:
            if not isinstance(i, dict):
                raise TypeError("""Tags must be provided as
                                a list of dictionaries.""")
            elif not self.valid_access_keys.issuperset(i.keys()):
                raise FormatError("Error in tag format.")
            elif not i["access"] in self.valid_net_access_vals:
                raise InvalidAccess(i["access"], self.valid_net_access_vals)


    def _admin_exists(self, admin_id):
        check = get_data(ext_url=self.url, headers=self.headers)
        try:
            for admin in check.json():
                if admin["email"] == admin_id or admin["id"] == admin_id:
                    return admin
        except ValueError:
            pass

        print "No admin %s found" % admin_id
        return None


    def add_admin(self, **kwargs):
        """ Define a new org-level Admin account on Dashboard under
            Organization -> Administrators.
            Args:
                name: Name of the new admin.
                email: Email of the new admin.
                access: Their access level; valid values are full, read-only, or
                none (for tag or network-level admins)
                networks: A list of dictionaries formatted as
                [network:network-id, access:access-level]; networks must be
                prexisting on Dashboard.
                tags: A list of dictionaries formatted as
                [{tag:tag-name}, {access:access-level}]; tags don't need to be
                prexisting on Dashboard.
            Returns:
                new_admin: a request object of the new admin's values
                as specified by the passed arguments and the HTTP
                return code for it, or None if the user already exists
        """

        self._provided_access_valid(kwargs["orgAccess"])
        if "tags" in kwargs.keys():
            self._provided_tags_valid(kwargs["tags"])
        if "networks" in kwargs.keys():
            pass # still deciding how this is going to get structured

        return requests.post(self.url, json=kwargs, headers=self.headers)


    def update_admin(self, admin_id, to_update):
        """Update an existing admin's permissions or access.
        Args:
            admin_id: A user ID string or email address.
            to_update: a dict of the fields to be updated; valid keys are
            orgAccess, name, tags, and network.
        Returns:
            updated: The request object of the updated admin, or None if the
            passed admin ID doesn't exist.
        """

        valid_updates = {"orgAccess", "name", "tag", "networks"}
        exists = self._admin_exists(admin_id)
        if not exists:
            return None
        elif not admin_id.isdigit():
            admin_id = exists["id"]

        update_url = self.url+admin_id

        if not isinstance(to_update, dict):
            raise FormatError("Updated parameters must be a dict.")

        elif not set(to_update.keys()).issubset(valid_updates):
            raise FormatError("Invalid user parameter specified.")
        if to_update.has_key("tag"):
            self._provided_tags_valid(to_update["tag"])
        if to_update.has_key("orgAccess"):
            self._provided_access_valid(to_update["orgAccess"])

        return requests.put(url=update_url, json=to_update,
                            headers=self.headers)


    def del_admin(self, admin_id):
        """ Delete a specified admin account.
            Args:
                admin_id: ID string or email of the admin to be deleted.
            Returns:
                deleted: The request object of the deleted admin, or None if the
                passed admin ID doesn't exist.
        """

        exists = self._admin_exists(admin_id)
        if not exists:
            return None
        elif not admin_id.isdigit():
            admin_id = exists["id"]

        url = self.url+admin_id

        return requests.delete(url, headers=self.headers)


