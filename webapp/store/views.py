from flask import Blueprint, render_template


jaasstore = Blueprint(
  'jaasstore', __name__,
  template_folder='/templates', static_folder='/static')


@jaasstore.route('/store')
def store():
    return render_template('store/store.html')


@jaasstore.route('/<charm_name>')
def details(charm_name):
    return render_template('store/details.html')
