from flask import Blueprint, abort, redirect, request, render_template
from webapp.store import models

from jujubundlelib import references

jaasstore = Blueprint(
    "jaasstore", __name__, template_folder="/templates", static_folder="/static"
)


@jaasstore.route("/store")
def store():
    return render_template("store/store.html")


@jaasstore.route("/search/")
def search():
    query = request.args.get('q', '').replace('/', ' ')
    entity_type = request.args.get('type', None)
    if entity_type not in ['charm', 'bundle']:
        entity_type = None
    series = request.args.get('series', None)
    tags = request.args.get('tags', None)
    sort = request.args.get('sort', None)
    provides = request.args.get('provides', None)
    requires = request.args.get('requires', None)
    if provides:
        results = models.fetch_provides(provides)
    elif requires:
        results = models.fetch_requires(requires)
    else:
        results = models.search_entities(query, entity_type=entity_type,
                                         tags=tags, sort=sort, series=series,
                                         promulgated_only=False)
    return render_template(
        'store/search.html',
        context={
            'current_series': series,
            'current_sort': sort,
            'current_type': entity_type,
            'results': results,
            'results_count':
                len(results['recommended']) + len(results['community']),
            'query': query
        }
    )


@jaasstore.route('/q/')
@jaasstore.route('/q/<path:path>')
def search_redirect(path=None):
    """
    Handle redirects from jujucharms.com search URLS to the jaas.ai format.
    e.g. /q/k8s/demo?sort=-name&series=xenial will redirect to
    /search?q=k8s+demo&sort=-name&series=xenial
    """
    query_string = []
    if path:
        query_string.append('q={}'.format(path.replace('/', '+')))
    if request.query_string:
        query_string.append(str(request.query_string, 'utf-8'))
    return redirect('/search?{}'.format('&'.join(query_string)), code=302)


@jaasstore.route("/u/<username>/")
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


@jaasstore.route("/u/<username>/<entity_name>/")
def user_entity(username, entity_name):
    reference = references.Reference.from_jujucharms_url(request.path[1:])
    entity = models.get_charm_or_bundle(reference)

    if entity:
        if entity["is_charm"]:
            # entity["display_name"] = ""
            # entity["revision_number"] = ""
            # entity["user"] = ""
            # entity["latest_revision_id"] = ""
            # entity["series"] = ""
            # entity["channel_details"] = ""
            entity["description"] = entity["charm_data"]["Meta"]["charm-metadata"][
                "Description"
            ]
            entity["user"] = entity["charm_data"]["Meta"]["owner"]["User"]
            return render_template(
                "store/charm-details.html", context={"entity": entity}
            )
        else:
            entity["user"] = entity["bundle_data"]["Meta"]["owner"]["User"]
            entity["id"] = entity["bundle_data"]["Id"]
            entity["series"] = entity["bundle_data"]["Meta"]["bundle-metadata"][
                "Series"
            ]
            entity["meta_published_info"] = entity["bundle_data"]["Meta"]["published"][
                "Info"
            ]
            return render_template(
                "store/bundle-details.html", context={"entity": entity}
            )
    else:
        return abort(404, "Entity not found {}".format())


@jaasstore.route("/<charm_or_bundle_name>")
@jaasstore.route("/<charm_or_bundle_name>/<series_or_version>")
@jaasstore.route("/<charm_or_bundle_name>/<series_or_version>/<version>")
def details(charm_or_bundle_name, series_or_version=None, version=None):
    reference = references.Reference.from_jujucharms_url(request.path[1:])
    entity = models.get_charm_or_bundle(reference)

    if entity:
        if entity["is_charm"]:
            entity["meta_published_info"] = entity["charm_data"]["Meta"]["published"][
                "Info"
            ]
            entity["description"] = entity["charm_data"]["Meta"]["charm-metadata"][
                "Description"
            ]
            return render_template(
                "store/charm-details.html", context={"entity": entity}
            )
        else:
            entity["user"] = entity["charm_data"]["Meta"]["owner"]["User"]
            entity["id"] = entity["bundle_data"]["Id"]
            entity["series"] = entity["bundle_data"]["Meta"]["bundle-metadata"][
                "Series"
            ]
            entity["meta_published_info"] = entity["bundle_data"]["Meta"]["published"][
                "Info"
            ]
            return render_template(
                "store/bundle-details.html", context={"entity": entity}
            )
    else:
        return abort(404, "Entity not found {}".format(charm_or_bundle_name))
