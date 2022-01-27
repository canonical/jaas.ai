from flask import Blueprint, redirect, request, abort


jaasredirects = Blueprint(
    "jaasredirects",
    __name__,
    template_folder="/templates",
    static_folder="/static",
)


@jaasredirects.route("/q/")
@jaasredirects.route("/q/<path:path>")
def search_redirect(path=None):
    """
    Handle redirects from jujucharms.com search URLS to the jaas.ai format.
    e.g. /q/k8s/demo?sort=-name&series=xenial will redirect to
    /search?q=k8s+demo&sort=-name&series=xenial
    """
    query_string = []
    if path:
        query_string.append("q={}".format(path.replace("/", "+")))
    if request.query_string:
        query_string.append(str(request.query_string, "utf-8"))
    return redirect("/search?{}".format("&".join(query_string)), code=302)


@jaasredirects.route("/u/<username>/<charm_or_bundle_name>")
@jaasredirects.route(
    "/u/<username>/<charm_or_bundle_name>/<series_or_version>"
)
@jaasredirects.route(
    "/u/<username>/<charm_or_bundle_name>/<series_or_version>/<version>"
)
def user_entity_redirect(
    username, charm_or_bundle_name, series_or_version=None, version=None
):
    charmhub_url = (
        "https://charmhub.io/" + username + "-" + charm_or_bundle_name
    )
    return redirect(charmhub_url, code=301)


@jaasredirects.route("/<charm_or_bundle_name>")
@jaasredirects.route("/<charm_or_bundle_name>/<series_or_version>")
@jaasredirects.route("/<charm_or_bundle_name>/<series_or_version>/<version>")
def details_redirect(
    charm_or_bundle_name,
    series_or_version=None,
    version=None,
):

    charmhub_url = "https://charmhub.io/" + charm_or_bundle_name
    return redirect(charmhub_url, code=301)
