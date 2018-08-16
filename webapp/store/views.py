from flask import Blueprint, render_template, abort, current_app
from theblues.charmstore import CharmStore
from pprint import pformat


jaasstore = Blueprint(
  'jaasstore', __name__,
  template_folder='/templates', static_folder='/static')

cs = CharmStore("https://api.jujucharms.com/v5")


@jaasstore.route('/store')
def store():
    return render_template('store/store.html')


@jaasstore.route('/<entity_name>')
def details(entity_name):
    try:
        entity = cs.entity(entity_name)
        entity_formatted = pformat(entity, 1, 120)
    except Exception:
        return abort(404, "Entity not found {}".format(entity_name))

    return render_template('store/details.html', entity=entity_formatted)
