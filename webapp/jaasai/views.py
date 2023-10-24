import talisker.requests
from flask import (
    Blueprint,
    current_app,
    make_response,
    render_template,
    request,
    send_from_directory,
)

jaasai = Blueprint(
    "jaasai", __name__, template_folder="/templates", static_folder="/static"
)

session = talisker.requests.get_session()


@jaasai.route("/")
def index():
    return render_template(
        "index.html"
    )


@jaasai.route("/robots.txt")
@jaasai.route("/favicon.ico")
def assets_from_root():
    return send_from_directory(current_app.static_folder, request.path[1:])


def set_xml_content_type(path, context={}):
    xml = render_template(path, context=context)
    response = make_response(xml)
    response.headers["Content-Type"] = "application/xml"
    return response


@jaasai.route("/sitemap.xml")
def sitemap():
    return set_xml_content_type("sitemaps/sitemap.xml")


@jaasai.route("/sitemap-base.xml")
def sitemap_base():
    context = {
        "pages": [
        ]
    }
    return set_xml_content_type("sitemaps/sitemap-base.xml", context)


@jaasai.route("/_status/check")
def health_check():
    """Health check end point used by Talisker."""
    return ("", 200)
