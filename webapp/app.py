import flask
import hashlib
import os
import prometheus_flask_exporter
import talisker.flask
from werkzeug.debug import DebuggedApplication
from werkzeug.middleware.proxy_fix import ProxyFix

from webapp.extensions import sentry
from webapp.external_urls import external_urls
from webapp.handlers import add_headers, clear_trailing_slash
from webapp.jaasai.views import jaasai
from webapp.redirects.views import jaasredirects
from webapp.store.views import jaasstore


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

        prometheus_flask_exporter.PrometheusMetrics(
            app,
            group_by_endpoint=True,
            buckets=[0.25, 0.5, 0.75, 1, 2],
            path=None,
        )

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

    def static_url(filename):
        """Template function for generating URLs to static assets:
            Given the path for a static file, output a url path
            with a hex hash as a query string for versioning.
            :param string: A file name.
            :returns: A file name with appended hash.
        """
        filepath = os.path.join("static", filename)
        url = flask.url_for("static", filename=filename)
        if not os.path.isfile(filepath):
            # Could not find static file.
            return url
        # Use MD5 as we care about speed a lot and not security in this case.
        file_hash = hashlib.md5()
        with open(filepath, "rb") as file_contents:
            for chunk in iter(lambda: file_contents.read(4096), b""):
                file_hash.update(chunk)
        return "{}?v={}".format(url, file_hash.hexdigest()[:7])

    @app.context_processor
    def inject_utilities():
        return {
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
