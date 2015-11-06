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

    from gitlab import GitLab

    # Load `username` and `password` from configuration file
    gitlab = GitLab(host='gitlab.cisco.com')
    print gitlab.get_current_user()
    {u'two_factor_enabled': False, u'can_create_project': True, u'twitter': u'', u'linkedin': u'', u'color_scheme_id': 1, u'web_url': u'http://gitlab.cisco.com/u/rightlag', u'skype': u'', u'identities': [{u'extern_uid': u'CN=jaswalsh,OU=Employees,OU=Cisco Users,DC=cisco,DC=com', u'provider': u'ldapmain'}], u'id': 6333, u'projects_limit': 10, u'current_sign_in_at': u'2015-11-03T01:03:37.539Z', u'state': u'active', u'email': u'jaswalsh@cisco.com', u'website_url': u'', u'username': u'rightlag', u'bio': u'', u'can_create_group': True, u'is_admin': False, u'name': u'Jason Walsh', u'created_at': u'2015-10-14T18:57:22.543Z', u'avatar_url': u'http://www.gravatar.com/avatar/64163a7584ac2c14735ecb0410889c50?s=40&d=identicon', u'private_token': u'V7x2bK_eYDULaWQzGxFs', u'theme_id': 2}
