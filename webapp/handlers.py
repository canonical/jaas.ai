import socket

import flask

CSP = {
    "default-src": ["'self'"],
    "script-src-elem": [
        "'self'",
        "assets.ubuntu.com",
        "buttons.github.io",
        "www.googletagmanager.com",
        "w.usabilla.com",
        "*.crazyegg.com",
        # This is necessary for Google Tag Manager to function properly.
        "'unsafe-inline'",
    ],
    "script-src": [
        "'unsafe-inline'",
        "blob:",
    ],
    "img-src": [
        "data: blob:",
        # This is needed to allow images from
        # https://www.google.*/ads/ga-audiences to load.
        "*",
    ],
    "font-src": [
        "'self'",
        "assets.ubuntu.com",
    ],
    "style-src": [
        "'self'",
        "'unsafe-inline'",
    ],
    "frame-src": [
        "'self'",
        "td.doubleclick.net",
        "www.youtube.com",
    ],
    "connect-src": [
        "'self'",
        "analytics.google.com",
        "stats.g.doubleclick.net",
        "www.googletagmanager.com",
        "sentry.is.canonical.com",
        "www.google-analytics.com",
        "*.crazyegg.com",
    ],
}


def get_csp_as_str(csp={}):
    csp_str = ""
    for key, values in csp.items():
        csp_value = " ".join(values)
        csp_str += f"{key} {csp_value}; "
    return csp_str.strip()


def add_headers(response):
    """
    Generic rules for headers to add to all requests

    - X-Hostname: Mention the name of the host/pod running the application
    - Cache-Control: Add cache-control headers for public and private pages
    - Content-Security-Policy: Restrict resources (e.g., JavaScript, CSS,
    Images) and URLs
    - Referrer-Policy: Limit referrer data for security while preserving
    full referrer for same-origin requests
    - Cross-Origin-Embedder-Policy: allows embedding cross-origin
    resources without credentials
    - Cross-Origin-Opener-Policy: enable the page to open pop-ups while
    maintaining same-origin policy
    - Cross-Origin-Resource-Policy: allowing only same-origin requests to
    access the resource
    - X-Permitted-Cross-Domain-Policies: disallows cross-domain access to
    resources
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

    response.headers["Content-Security-Policy"] = get_csp_as_str(CSP)
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Cross-Origin-Embedder-Policy"] = "credentialless"
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin-allow-popups"
    response.headers["Cross-Origin-Resource-Policy"] = "same-site"
    response.headers["X-Permitted-Cross-Domain-Policies"] = "none"

    return response
