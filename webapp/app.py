import flask
import talisker.flask
import talisker.logs
from werkzeug.debug import DebuggedApplication
from werkzeug.middleware.proxy_fix import ProxyFix

from webapp.extensions import sentry
from webapp.external_urls import external_urls
from webapp.handlers import add_headers, clear_trailing_slash
from webapp.jaasai.views import jaasai
from webapp.redirects.views import jaasredirects
from webapp.store.views import jaasstore
from webapp.template_utils import current_url_with_query, static_url


def create_app(testing=False):
    app = flask.Flask(
        __name__, template_folder="../templates", static_folder="../static"
    )

    app.testing = testing

    app.wsgi_app = ProxyFix(app.wsgi_app)
    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app)

    app.url_map.strict_slashes = False

    if not testing:
        talisker.flask.register(app)
        talisker.logs.set_global_extra({"service": "jaas.ai"})

        init_extensions(app)

    app.before_request(clear_trailing_slash)
    app.after_request(add_headers)

    init_handler(app)
    init_blueprint(app)

    @app.template_filter("pluralize")
    def pluralize(count):
        if count != 1:
            return "s"
        return ""

    @app.context_processor
    def inject_utilities():
        return {
            "current_url_with_query": current_url_with_query,
            "external_urls": external_urls,
            "static_url": static_url,
        }

    app.jinja_env.add_extension("jinja2.ext.do")

    return app


def init_handler(app):
    @app.errorhandler(404)
    def page_not_found(error):
        """
        For 404 pages, display the 404.html template,
        passing through the error description.
        """

        return flask.render_template("404.html", error=error.description), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        """
        For 500 pages, display the 500.html template,
        passing through the error.
        """

        return flask.render_template("500.html", error=error), 500


def init_blueprint(app):
    app.register_blueprint(jaasai)
    app.register_blueprint(jaasredirects)
    app.register_blueprint(jaasstore)


def init_extensions(app):
    sentry.init_app(app)
