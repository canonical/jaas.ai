import socket

import flask


def add_headers(response):
    """
    Generic rules for headers to add to all requests

    - X-Hostname: Mention the name of the host/pod running the application
    - Cache-Control: Add cache-control headers for public and private pages
    """

    response.headers["X-Hostname"] = socket.gethostname()

    if response.status_code == 200:
        if flask.session:
            response.headers["Cache-Control"] = "private"
        else:
            # Only add caching headers to successful responses
            response.headers["Cache-Control"] = ", ".join(
                {
                    "public",
                    "max-age=61",
                    "stale-while-revalidate=300",
                    "stale-if-error=86400",
                }
            )

    return response
