"""
A Flask application for snapcraft.io.

The web frontend for the snap store.
"""

# Third-party packages
import flask
import talisker.flask
import prometheus_flask_exporter
from flask import render_template
from raven.contrib.flask import Sentry
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.debug import DebuggedApplication

# Local webapp
import webapp.routing as helpers
from webapp.handlers import (
    add_headers,
    clear_trailing_slash
)


app = flask.Flask(
    __name__,
    template_folder='../templates',
    static_folder='../static')

app.config.from_object('webapp.config')

app.wsgi_app = ProxyFix(app.wsgi_app)
if app.debug:
    app.wsgi_app = DebuggedApplication(app.wsgi_app)

app.url_map.strict_slashes = False
app.url_map.converters['regex'] = helpers.RegexConverter

talisker.flask.register(app)

prometheus_flask_exporter.PrometheusMetrics(
    app,
    group_by_endpoint=True,
    buckets=[0.25, 0.5, 0.75, 1, 2],
    path=None
)

Sentry().init_app(app)

# Generic handlers
app.before_request(clear_trailing_slash)
app.after_request(add_headers)


@app.errorhandler(404)
def page_not_found(error):
    """
    For 404 pages, display the 404.html template,
    passing through the error description.
    """

    return flask.render_template(
        '404.html', error=error.description
    ), 404


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/experts')
def experts():
    return render_template('experts.html')

@app.route('/how-it-works')
def how_it_works():
    return render_template('how-it-works.html')

@app.route('/community')
def community():
    return render_template('community.html')

@app.route('/jaas')
def jaas():
    return render_template('jaas.html')

@app.route('/store')
def store():
    return render_template('store.html')
