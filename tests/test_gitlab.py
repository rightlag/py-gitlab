import unittest

from datetime import datetime
from gitlab import GitLab
from gitlab.decorators import namespace
from gitlab.exceptions import GitLabServerError
from gitlab.settings import ConfigParser


class GitLabTestCase(unittest.TestCase):
    def setUp(self):
        self.config = ConfigParser()
        self.config.read('~/.gitlab')
        self.gitlab = GitLab(host='gitlab.com')

    def test_authentication_error_is_raised_with_invalid_private_token(self):
        """
        Assert that a `401 Unauthorized` exception is raised provided the user
        enters invalid credentials
        """
        with self.assertRaises(GitLabServerError) as e:
            gitlab = GitLab(host='gitlab.com', private_token='foobar')
            gitlab.get_current_user()
        exception = e.exception
        self.assertEqual(exception.status_code, 401)
        self.assertEqual(exception.reason, 'Unauthorized')

    def test_private_token_http_header_exists(self):
        """
        Assert that the `PRIVATE-TOKEN` header exists in the HTTP request
        header and that it is not `None`
        """
        self.assertTrue('PRIVATE-TOKEN' in self.gitlab._session.headers)
        self.assertIsNotNone(self.gitlab._session.headers['PRIVATE-TOKEN'])

    def test_get_users_endpoint_with_query_params(self):
        """
        Assert that the result set returned with query params is as expected
        """
        users = self.gitlab.get_users(per_page=1)
        self.assertEqual(len(users), 1)

    def test_get_user_endpoint_with_invalid_id(self):
        """
        Assert that `400 Bad Request` is raised when retrieving a user with
        invalid ID
        """
        with self.assertRaises(GitLabServerError) as e:
            self.gitlab.get_user(id=-1)
        exception = e.exception
        self.assertEqual(exception.status_code, 400)
        self.assertEqual(exception.reason, 'Bad Request')

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
