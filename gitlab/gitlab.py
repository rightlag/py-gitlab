# -*- coding: utf-8 -*-
import requests

from decorators import namespace
from exceptions import GitLabServerError
from settings import Config


class GitLab(object):
    Version = 'v3'
    ResponseError = GitLabServerError

    def __init__(self, host=None, username=None, password=None):
        config = Config()
        self.host = config.default_host if not host else host
        if not (username or password):
            # Username and/or password not assigned
            # try environment variables
            username = config.get('username')
            password = config.get('password')
        # Authenticate the user via HTTP basic authentication
        self.authenticate(username, password)

    @property
    def _base_url(self):
        """Set the GitLab API base URL."""
        protocol = 'https'
        base_url = '{protocol}://{host}/api/{version}'.format(
            protocol=protocol, host=self.host, version=self.Version
        )
        return base_url

    def authenticate(self, username, password):
        """Authenticate user via HTTP Basic Authentication."""
        auth_url = self._base_url.rsplit('/', 2)[0]
        path = '/oauth/token'
        data = {
            'grant_type': 'password',
            'username': username,
            'password': password,
        }
        res = requests.post(auth_url + path, data=data)
        if res.status_code != 200:
            # Authentication failed
            # raise `GitLabServerError`
            raise self.ResponseError(res.status_code, res.reason)
        # Create a `Session` object to persist certain parameters across
        # requests
        self._session = requests.Session()
        # Set HTTP `Authorization` request header for the `Session` object
        self._session.headers.update({
            'Authorization': '{res[token_type]} {res[access_token]}'.format(
                res=res.json()
            )
        })

    def get_users(self, **kwargs):
        """Get a list of users."""
        path = '/users'
        data = self._request('GET', path, **kwargs)
        return data

    def get_user(self, id=None):
        """Get a single user."""
        path = '/users/{id}'.format(id=id)
        data = self._request('GET', path)
        return data

    def get_current_user(self):
        """Gets currently authenticated user."""
        path = '/user'
        data = self._request('GET', path)
        return data

    def get_projects(self, **kwargs):
        """Get a list of projects accessible by the authenticated user."""
        path = '/projects'
        data = self._request('GET', path, **kwargs)
        return data

    def get_owned_projects(self, **kwargs):
        """Get a list of projects which are owned by the authenticated user."""
        path = '/projects/owned'
        data = self._request('GET', path, **kwargs)
        return data

    def get_all_projects(self, **kwargs):
        """Get a list of all GitLab projects (admin only)."""
        path = '/projects/all'
        data = self._request('GET', path, **kwargs)
        return data

    @namespace
    def get_project(self, id=None):
        """Get a specific project which is owned by the authenticated user."""
        path = '/projects/{id}'.format(id=id)
        data = self._request('GET', path)
        return data

    @namespace
    def get_project_events(self, id=None):
        """Get the events for the specified project. Sorted from newest to
        latest."""
        path = '/projects/{id}/events'.format(id=id)
        data = self._request('GET', path)
        return data

    @namespace
    def get_project_team_members(self, id=None, **kwargs):
        """Get a list of a project's team members."""
        path = '/projects/{id}/members'.format(id=id)
        data = self._request('GET', path, **kwargs)
        return data

    @namespace
    def get_project_team_member(self, id=None, user_id=None):
        """Gets a project team member."""
        path = '/projects/{id}/members/{user_id}'.format(
            id=id, user_id=user_id
        )
        data = self._request('GET', path)
        return data

    @namespace
    def get_branches(self, id=None):
        """Lists all branches of a project."""
        path = '/projects/{id}/repository/branches'.format(id=id)
        data = self._request('GET', path)
        return data

    @namespace
    def get_branch(self, id=None, branch=None):
        """Lists a specific branch of a project."""
        path = '/projects/{id}/repository/branches/{branch}'.format(
            id=id, branch=branch
        )
        data = self._request('GET', path)
        return data

    def _request(self, method, url, data={}, **kwargs):
        """Wrapper method for making requests to endpoints."""
        url = self._base_url + url
        res = self._session.request(method, url, params=kwargs, data=data)
        if res.status_code not in [200, 201]:
            raise self.ResponseError(res.status_code, res.reason)
        if res.headers['Content-Type'] != 'application/json':
            # Redirects cached
            if res.history:
                # The response always returns 200 OK even if it contains
                # redirects
                # If the response `history` attribute is `True` assume
                # 404 Not Found
                raise self.ResponseError(404, 'Not Found')
        try:
            return res.json()
        except ValueError, e:
            # JSON object can't be deserialized
            # raise exception
            raise e

    def __str__(self):
        return '{}:{}'.format(self.__class__.__name__, self.host)

    def __repr__(self):
        return self.__str__()
