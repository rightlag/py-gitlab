# py-gitlab

py-gitlab 0.1.0

Released: 3-Nov-2015

---

# Introduction

py-gitlab is a Python package that provides an interface to the [GitLab RESTful web API](https://github.com/gitlabhq/gitlabhq/tree/master/doc/api).

# Getting started with py-gitlab

Your credentials can be passed when instantiating the GitLab class. Alternatively, py-gitlab will check for the existence of a configuration file named `~/.gitlab`. The configuration file is JSON formatted:

    {
        "username": <Your GitLab username>,
        "password": <Your GitLab password>
    }

# Sample endpoint request

### Get the current user

**Note:** `username` and `password` are loaded from `~/.gitlab` configuration file

    from gitlab import GitLab

    gitlab = GitLab(host='gitlab.com')
    print gitlab.get_current_user()
    {u'two_factor_enabled': False, u'can_create_project': True, u'twitter': u'', u'linkedin': u'', u'color_scheme_id': 1, u'web_url': u'https://gitlab.com/u/rightlag', u'skype': u'', u'identities': [{u'extern_uid': u'2184329', u'provider': u'github'}], u'id': 297563, u'projects_limit': 100000, u'current_sign_in_at': u'2015-11-04T04:53:37.301Z', u'state': u'active', u'email': u'rightlag@gmail.com', u'website_url': u'', u'username': u'rightlag', u'bio': None, u'can_create_group': True, u'is_admin': False, u'name': u'Jason Walsh', u'created_at': u'2015-11-04T03:23:03.215Z', u'avatar_url': u'https://secure.gravatar.com/avatar/90a2082cd36795676d8bd2be5f01e569?s=40&d=identicon', u'private_token': u'NxzSYh7ZQBszW34HU2vJ', u'theme_id': 2}

### Get projects owned by current user

    print gitlab.get_projects()
    [{u'forks_count': 0, u'http_url_to_repo': u'https://gitlab.com/rightlag/foo-bar.git', u'web_url': u'https://gitlab.com/rightlag/foo-bar', u'owner': {u'username': u'rightlag', u'web_url': u'https://gitlab.com/u/rightlag', u'name': u'Jason Walsh', u'state': u'active', u'avatar_url': u'https://secure.gravatar.com/avatar/90a2082cd36795676d8bd2be5f01e569?s=40&d=identicon', u'id': 297563}, u'wiki_enabled': True, u'id': 580202, u'merge_requests_enabled': True, u'archived': False, u'snippets_enabled': False, u'namespace': {u'share_with_group_lock': False, u'name': u'rightlag', u'created_at': u'2015-11-04T03:23:03.288Z', u'description': u'', u'updated_at': u'2015-11-04T03:23:03.288Z', u'avatar': None, u'membership_lock': False, u'path': u'rightlag', u'id': 350244, u'owner_id': 297563}, u'star_count': 0, u'issues_enabled': True, u'path_with_namespace': u'rightlag/foo-bar', u'public': False, u'description': u'', u'default_branch': None, u'ssh_url_to_repo': u'git@gitlab.com:rightlag/foo-bar.git', u'path': u'foo-bar', u'visibility_level': 0, u'last_activity_at': u'2015-11-07T02:50:37.158Z', u'name': u'foo-bar', u'name_with_namespace': u'Jason Walsh / foo-bar', u'created_at': u'2015-11-07T02:50:37.158Z', u'creator_id': 297563, u'avatar_url': None, u'tag_list': []}]

### Get project with namespace (e.g. `rightlag/foo-bar`)

    print gitlab.get_project(id='rightlag/foo-bar')
    {u'forks_count': 0, u'http_url_to_repo': u'https://gitlab.com/rightlag/foo-bar.git', u'web_url': u'https://gitlab.com/rightlag/foo-bar', u'owner': {u'username': u'rightlag', u'web_url': u'https://gitlab.com/u/rightlag', u'name': u'Jason Walsh', u'state': u'active', u'avatar_url': u'https://secure.gravatar.com/avatar/90a2082cd36795676d8bd2be5f01e569?s=40&d=identicon', u'id': 297563}, u'wiki_enabled': True, u'id': 580202, u'merge_requests_enabled': True, u'archived': False, u'snippets_enabled': False, u'namespace': {u'share_with_group_lock': False, u'name': u'rightlag', u'created_at': u'2015-11-04T03:23:03.288Z', u'description': u'', u'updated_at': u'2015-11-04T03:23:03.288Z', u'avatar': None, u'membership_lock': False, u'path': u'rightlag', u'id': 350244, u'owner_id': 297563}, u'star_count': 0, u'issues_enabled': True, u'path_with_namespace': u'rightlag/foo-bar', u'public': False, u'description': u'', u'default_branch': None, u'ssh_url_to_repo': u'git@gitlab.com:rightlag/foo-bar.git', u'path': u'foo-bar', u'visibility_level': 0, u'permissions': {u'group_access': None, u'project_access': {u'notification_level': 3, u'access_level': 40}}, u'last_activity_at': u'2015-11-07T02:50:37.158Z', u'name': u'foo-bar', u'name_with_namespace': u'Jason Walsh / foo-bar', u'created_at': u'2015-11-07T02:50:37.158Z', u'creator_id': 297563, u'avatar_url': None, u'tag_list': []}
