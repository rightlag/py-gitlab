import os
import unittest

from gitlab import GitLab
from gitlab.exceptions import GitLabServerError
from gitlab.settings import get_ldap_username


class GitLabTestCase(unittest.TestCase):
    def setUp(self):
        self.gitlab = GitLab(host='gitlab.cisco.com')

    def test_authentication_error_is_raised_with_invalid_credentials(self):
        """
        Assert that a `401 Unauthorized` exception is raised provided the user
        enters invalid credentials
        """
        with self.assertRaises(GitLabServerError) as e:
            username = 'foo'
            password = 'bar'
            GitLab(username=username, password=password)
        exception = e.exception
        self.assertEqual(exception.status_code, 401)
        self.assertEqual(exception.reason, 'Unauthorized')

    def test_authorization_bearer_token_exists(self):
        """
        Assert that the `Authorization` header exists in the HTTP request
        header and that it is not `None`
        """
        self.assertTrue('Authorization' in self.gitlab._session.headers)
        self.assertIsNotNone(self.gitlab._session.headers['Authorization'])

    def test_configuration_error_is_raised_without_environment_variables(self):
        """
        Assert that a `401 Unauthorized` exception is raised given that the
        GitLab environment variables are not set
        """
        # Remove the environment variables from the dictionary object
        username = os.environ.pop('GITLAB_USERNAME')
        password = os.environ.pop('GITLAB_PASSWORD')
        with self.assertRaises(GitLabServerError):
            GitLab()
        # Reassign the environment variables for they are required in
        # additional tests
        os.environ['GITLAB_USERNAME'] = username
        os.environ['GITLAB_PASSWORD'] = password

    def test_get_current_user(self):
        """
        Assert that the `get_current_user` method returns the appropriate user
        authenticated via ldap
        """
        # First issue the `get_current_user` method
        user = self.gitlab.get_current_user()
        ldap_username = get_ldap_username(user)
        self.assertEqual(os.environ['GITLAB_USERNAME'], ldap_username)

    def test_get_users_endpoint_with_query_params(self):
        users = self.gitlab.get_users(per_page=1)
        self.assertEqual(len(users), 1)
