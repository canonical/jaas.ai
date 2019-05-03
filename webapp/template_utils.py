import hashlib
import os
from flask import request, url_for
from werkzeug.urls import url_encode


def static_url(filename):
    """Template function for generating URLs to static assets:
        Given the path for a static file, output a url path
        with a hex hash as a query string for versioning.
        :param string: A file name.
        :returns: A file name with appended hash.
    """
    filepath = os.path.join("static", filename)
    url = url_for("static", filename=filename)
    if not os.path.isfile(filepath):
        # Could not find static file.
        return url
    # Use MD5 as we care about speed a lot and not security in this case.
    file_hash = hashlib.md5()
    with open(filepath, "rb") as file_contents:
        for chunk in iter(lambda: file_contents.read(4096), b""):
            file_hash.update(chunk)
    return "{}?v={}".format(url, file_hash.hexdigest()[:7])


def current_url_with_query(**query_params):
    """Generate a version of the current URL with modified query params. This
        can be used for changing search filters when you want to maintain
        other existing filters.
        :param **kwargs: The query params to manipulate.
        :returns: A new URL.
    """
    params = request.args.copy()
    for param, value in query_params.items():
        params[param] = value
    return "{}?{}".format(request.path, url_encode(params))
