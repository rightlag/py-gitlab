import unittest

from datetime import datetime
from gitlab import GitLab
from gitlab.decorators import namespace
from gitlab.exceptions import GitLabServerError
from gitlab.settings import ConfigParser, get_ldap_username


class GitLabTestCase(unittest.TestCase):
    def setUp(self):
        self.gitlab = GitLab(host='gitlab.cisco.com')
        self.config = ConfigParser()
        self.config.read('~/.gitlab')

    def test_authentication_error_is_raised_with_invalid_credentials(self):
        """
        Assert that a `401 Unauthorized` exception is raised provided the user
        enters invalid credentials
        """
        with self.assertRaises(GitLabServerError) as e:
            username = 'foo'
            password = 'bar'
            GitLab(host='gitlab.cisco.com', username=username,
                   password=password)
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

    def test_get_current_user(self):
        """
        Assert that the `get_current_user` method returns the appropriate user
        authenticated via ldap
        """
        user = self.gitlab.get_current_user()
        ldap_username = get_ldap_username(user)
        self.assertEqual(self.config.get('username'), ldap_username)

    def test_get_users_endpoint_with_query_params(self):
        """
        Assert that the result set returned with query params is as expected
        """
        users = self.gitlab.get_users(per_page=1)
        self.assertEqual(len(users), 1)

    def test_get_projects_endpoint_with_query_params(self):
        """
        Assert that the result set returned with query params is as expected
        """
        projects = self.gitlab.get_projects(sort='asc')
        format_spec = '%Y-%m-%dT%H:%M:%S.%fZ'
        # Convert ISO formatted `datetime` strings into `datetime` objects
        projects = [
            datetime.strptime(project['created_at'], format_spec)
            for project in projects
        ]
        # Need to create a copy to not modify the original `projects` list
        # object
        projects_copy = list(projects)
        # Assert that the `projects` are sorted in ascending order
        self.assertEqual(projects, sorted(projects_copy))
        projects = self.gitlab.get_projects(sort='desc')
        projects = [
            datetime.strptime(project['created_at'], format_spec)
            for project in projects
        ]
        # `reversed` function returns a generator object, need to convert to a
        # `list` object
        self.assertEqual(projects, list(reversed(projects_copy)))

    def test_namespace_decorator(self):
        """
        Assert that project namespaces are URL encoded
        (e.g. / is represented by %2F)
        """
        @namespace
        def foo(id=None):
            self.assertTrue('%2F' in id)
        foo.__call__(id='foo/bar')
