class GitLabServerError(Exception):
    def __init__(self, status_code, reason):
        self.status_code = status_code
        self.reason = reason

    def __str__(self):
        return '{} {}'.format(self.status_code, self.reason)
