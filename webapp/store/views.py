from flask import (
    Blueprint,
    abort,
    redirect,
    request,
    render_template,
    Response,
)

from webapp.experts import get_experts
from webapp.store import models

jaasstore = Blueprint(
    "jaasstore",
    __name__,
    template_folder="/templates",
    static_folder="/static",
)


@jaasstore.route("/store")
def store():
    return render_template(
        "store/store.html", context={"experts": get_experts()}
    )


@jaasstore.route("/search")
def search():
    query = request.args.get("q", "")
    charmhub_url = "https://charmhub.io/?q=" + query
    return redirect(charmhub_url, code=301)


@jaasstore.route("/u/<username>")
def user_details(username):
    return abort(410, "User pages have been depricated")


@jaasstore.route("/u/<username>/<charm_or_bundle_name>")
@jaasstore.route("/u/<username>/<charm_or_bundle_name>/<series_or_version>")
@jaasstore.route(
    "/u/<username>/<charm_or_bundle_name>/<series_or_version>/<version>"
)
def user_entity(
    username, charm_or_bundle_name, series_or_version=None, version=None
):
    charmhub_url = (
        "https://charmhub.io/" + username + "-" + charm_or_bundle_name
    )
    return redirect(charmhub_url, code=301)


@jaasstore.route("/terms/<string:name>")
@jaasstore.route("/terms/<string:name>/<int:revision>")
def terms(name, revision=None):
    terms = models.get_terms(name, revision)
    if terms:
        return Response(terms, mimetype="text/plain")
    else:
        return abort(404, "Terms not found {}".format(name))


@jaasstore.route("/<charm_or_bundle_name>")
@jaasstore.route("/<charm_or_bundle_name>/<series_or_version>")
@jaasstore.route("/<charm_or_bundle_name>/<series_or_version>/<version>")
def details(
    charm_or_bundle_name,
    series_or_version=None,
    version=None,
):

    charmhub_url = "https://charmhub.io/" + charm_or_bundle_name
    return redirect(charmhub_url, code=301)
