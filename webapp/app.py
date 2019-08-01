import flask
import datetime

from canonicalwebteam.blog.app import BlogExtension
from canonicalwebteam.flask_base.app import FlaskBase
from canonicalwebteam.yaml_responses.flask_helpers import (
    prepare_deleted,
    prepare_redirects,
)
from webapp.external_urls import external_urls
from webapp.handlers import add_headers
from webapp.jaasai.views import jaasai
from webapp.redirects.views import jaasredirects
from webapp.store.views import jaasstore
from webapp.template_utils import current_url_with_query, static_url
from webapp.docs.views import init_docs


def create_app(testing=False):
    app = FlaskBase(
        __name__,
        "jaas.ai",
        template_folder="../templates",
        static_folder="../static",
    )

    app.testing = testing
    app.after_request(add_headers)
    app.before_request(prepare_redirects())
    app.before_request(prepare_deleted())

    BlogExtension(app, "JAAS Case Studies", [""], "lang:en", "/case-studies")

    init_handler(app)
    init_blueprint(app)

    @app.template_filter("pluralize")
    def pluralize_filter(count):
        if int(count) > 1:
            return "s"
        else:
            return ""

    @app.context_processor
    def inject_utilities():
        return {
            "current_url_with_query": current_url_with_query,
            "external_urls": external_urls,
            "static_url": static_url,
        }

    @app.context_processor
    def inject_today_date():
        return {"current_year": datetime.date.today().year}

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
    init_docs(app, "/docs")
