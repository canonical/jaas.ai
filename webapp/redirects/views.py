from flask import Blueprint, redirect, request, abort


jaasredirects = Blueprint(
    "jaasredirects",
    __name__,
    template_folder="/templates",
    static_folder="/static",
)


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
