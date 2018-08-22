from flask import Blueprint, abort, request, render_template
from webapp.store import models

from jujubundlelib import references


jaasstore = Blueprint(
  'jaasstore', __name__,
  template_folder='/templates', static_folder='/static')


@jaasstore.route('/store')
def store():
    return render_template('store/store.html')


@jaasstore.route('/u/<user_name>/<entity_name>/')
def user_details():
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
