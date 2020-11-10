import requests
from flask import Blueprint, abort, request, render_template, Response
from jujubundlelib import references

from webapp.experts import get_experts
from webapp.store import models

jaasstore = Blueprint(
    "jaasstore",
    __name__,
    template_folder="/templates",
    static_folder="/static",
)

SERIES = [
    "artful",
    "bionic",
    "centos7",
    "cosmic",
    "disco",
    "eoan",
    "kubernetes",
    "oneiric",
    "precise",
    "quantal",
    "raring",
    "saucy",
    "trusty",
    "utopic",
    "vivid",
    "wily",
    "win10",
    "win2012",
    "win2012hv",
    "win2012hvr2",
    "win2012r2",
    "win2016",
    "win2016hv",
    "win2016nano",
    "win7",
    "win8",
    "win81",
    "xenial",
    "yakkety",
    "zesty",
]


@jaasstore.route("/store")
def store():
    return render_template(
        "store/store.html", context={"experts": get_experts()}
    )


@jaasstore.route("/search")
def search():
    query = request.args.get("q", "")
    search_terms = query.replace("/", " ")
    entity_type = request.args.get("type", None)
    if entity_type not in ["charm", "bundle"]:
        entity_type = None
    series = request.args.get("series", None)
    tags = request.args.get("tags", None)
    sort = request.args.get("sort", None)
    provides = request.args.get("provides", None)
    requires = request.args.get("requires", None)
    if provides:
        results = models.fetch_provides(provides)
    elif requires:
        results = models.fetch_requires(requires)
    else:
        results = models.search_entities(
            search_terms,
            entity_type=entity_type,
            tags=tags,
            sort=sort,
            series=series,
            promulgated_only=False,
        )
    if len(results["recommended"]) + len(results["community"]) == 0:
        # If there are no results then check to see if this string could be a
        # bundle/charm id and do another search. This is something the
        # charmstore should handle internally, but until it does, do it here.
        reference = models.get_reference(query)
        if reference is not None:
            results = models.search_entities(
                reference.name,
                owner=reference.user,
                entity_type=entity_type,
                tags=tags,
                sort=sort,
                series=series,
                promulgated_only=False,
            )
    return render_template(
        "store/search.html",
        context={
            "all_series": SERIES,
            "current_series": series,
            "current_sort": sort,
            "current_type": entity_type,
            "results": results,
            "results_count": len(results["recommended"])
            + len(results["community"]),
            "query": query,
        },
    )


@jaasstore.route("/u/<username>")
def user_details(username):
    entities = models.get_user_entities(username)
    if len(entities["charms"]) > 0 or len(entities["bundles"]) > 0:
        return render_template(
            "store/user-details.html",
            context={
                "bundles_count": len(entities["bundles"]),
                "bundles": entities["bundles"],
                "charms_count": len(entities["charms"]),
                "charms": entities["charms"],
                "entities": entities,
                "username": username,
            },
        )
    else:
        return abort(404, "User not found: {}".format(username))


@jaasstore.route("/u/<username>/<charm_or_bundle_name>")
@jaasstore.route("/u/<username>/<charm_or_bundle_name>/<series_or_version>")
@jaasstore.route(
    "/u/<username>/<charm_or_bundle_name>/<series_or_version>/<version>"
)
def user_entity(
    username, charm_or_bundle_name, series_or_version=None, version=None
):
    return details(
        charm_or_bundle_name,
        series_or_version=series_or_version,
        version=version,
    )


@jaasstore.route("/<charm_or_bundle_name>")
@jaasstore.route("/<charm_or_bundle_name>/<series_or_version>")
@jaasstore.route("/<charm_or_bundle_name>/<series_or_version>/<version>")
def details(charm_or_bundle_name, series_or_version=None, version=None):
    reference = None
    try:
        reference = references.Reference.from_jujucharms_url(request.path[1:])
    except ValueError:
        pass

    entity = None
    if reference:
        entity = models.get_charm_or_bundle(reference)

    if entity:
        try:
            response = requests.get(
                (
                    f"https://api.snapcraft.io/v2/charms/info/"
                    f"{charm_or_bundle_name}"
                )
            )
            exists_in_charmhub = response.status_code == 200
        except Exception:
            exists_in_charmhub = False

        template = "store/{}-details.html".format(
            "charm" if entity.is_charm else "bundle"
        )
        return render_template(
            template,
            context={
                "entity": entity,
                "expert": get_experts(entity.owner),
                "charm_bundle_name": charm_or_bundle_name,
                "exists_in_charmhub": exists_in_charmhub,
            },
        )
    else:
        return abort(404, "Entity not found {}".format(charm_or_bundle_name))


@jaasstore.route("/terms/<string:name>")
@jaasstore.route("/terms/<string:name>/<int:revision>")
def terms(name, revision=None):
    terms = models.get_terms(name, revision)
    if terms:
        return Response(terms, mimetype="text/plain")
    else:
        return abort(404, "Terms not found {}".format(name))
