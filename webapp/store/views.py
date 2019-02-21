from flask import Blueprint, abort, request, render_template
from webapp.store import models

from jujubundlelib import references


jaasstore = Blueprint(
  'jaasstore', __name__,
  template_folder='/templates', static_folder='/static')


@jaasstore.route('/store')
def store():
    return render_template('store/store.html')


@jaasstore.route('/u/<username>/')
def user_details(username):
    entities = models.get_user_entities(username)
    if len(entities['charms']) > 0 and len(entities['bundles']) > 0:
        return render_template(
            'store/user-details.html',
            context={
                'bundles_count': len(entities['bundles']),
                'bundles': entities['bundles'],
                'charms_count': len(entities['charms']),
                'charms': entities['charms'],
                'entities': entities,
                'username': username
            }
        )
    else:
        return abort(404, "User not found: {}".format(username))


@jaasstore.route('/u/<username>/<entity_name>/')
def user_entity(username, entity_name):
    raise NotImplementedError()


@jaasstore.route('/<charm_or_bundle_name>')
@jaasstore.route('/<charm_or_bundle_name>/<series_or_version>')
@jaasstore.route('/<charm_or_bundle_name>/<series_or_version>/<version>')
def details(charm_or_bundle_name, series_or_version=None, version=None):
    reference = references.Reference.from_jujucharms_url(request.path[1:])
    charm_or_bundle = models.get_charm_or_bundle(reference)

    if charm_or_bundle:
        if charm_or_bundle['is_charm']:
            return render_template(
                'store/charm-details.html',
                context={'charm': charm_or_bundle}
            )
        else:
            return render_template(
                'store/bundle-details.html',
                context={'bundle': charm_or_bundle}
            )
    else:
        return abort(404, "Entity not found {}".format(charm_or_bundle_name))
