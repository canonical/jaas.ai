import flask
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.debug import DebuggedApplication

import prometheus_flask_exporter
import talisker.flask
from webapp.extensions import sentry
from webapp.handlers import add_headers, clear_trailing_slash
from webapp.jaasai.views import jaasai
from webapp.store.views import jaasstore


def create_app(testing=False):
    app = flask.Flask(
        __name__, template_folder='../templates', static_folder='../static')

    app.testing = testing

    app.wsgi_app = ProxyFix(app.wsgi_app)
    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app)

    app.url_map.strict_slashes = False

    if not testing:
        talisker.flask.register(app)

        prometheus_flask_exporter.PrometheusMetrics(
            app,
            group_by_endpoint=True,
            buckets=[0.25, 0.5, 0.75, 1, 2],
            path=None
        )

        init_extensions(app)

    app.before_request(clear_trailing_slash)
    app.after_request(add_headers)

    init_handler(app)
    init_blueprint(app)

    @app.template_filter('pluralize')
    def pluralize(count):
        if count != 1:
            return 's'
        return ''

    return app


def init_handler(app):
    @app.errorhandler(404)
    def page_not_found(error):
        """
        For 404 pages, display the 404.html template,
        passing through the error description.
        """

        return flask.render_template(
            '404.html', error=error.description
        ), 404


def init_blueprint(app):
    app.register_blueprint(jaasai)
    app.register_blueprint(jaasstore)


def init_extensions(app):
    sentry.init_app(app)
