import urllib

from functools import wraps


def namespace(fn):
    """
    If using namespaced projects call make sure that the
    NAMESPACE/PROJECT_NAME is URL-encoded.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'id' in kwargs:
            kwargs['id'] = urllib.urlencode(id)
        return fn(*args, **kwargs)
    return wrapper
