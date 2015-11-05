import os


class BaseConfig(object):
    env_prefix = 'GITLAB_'

    @property
    def default_host(self):
        return 'gitlab.com'

    def get(self, key):
        key = key.upper()
        try:
            return os.environ[self.env_prefix + key]
        except KeyError:
            return None


class DevelopmentConfig(BaseConfig):
    pass


def get_ldap_username(user):
    """Return the Active Directory username from the GitLab account."""
    try:
        return user['identities'][0]['extern_uid'].split(',')[0][3:]
    except IndexError:
        return None
