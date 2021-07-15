import flask
import datetime

import talisker
from canonicalwebteam.blog import build_blueprint, BlogViews, BlogAPI
from canonicalwebteam.flask_base.app import FlaskBase
from canonicalwebteam.yaml_responses.flask_helpers import (
    prepare_deleted,
    prepare_redirects,
)
from canonicalwebteam import image_template

from webapp.external_urls import external_urls
from webapp.handlers import add_headers
from webapp.jaasai.views import jaasai
from webapp.redirects.views import jaasredirects
from webapp.store.models import cs
from webapp.store.views import jaasstore
from webapp.template_utils import current_url_with_query, static_url

session = talisker.requests.get_session()


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

    blog_views = BlogViews(
        api=BlogAPI(
            session=session,
            thumbnail_width=354,
            thumbnail_height=180,
        ),
        blog_title="JAAS Case Studies",
        tag_ids=[3513],
        feed_description="Case Studies from happy JAAS users",
    )
    app.register_blueprint(
        build_blueprint(blog_views), url_prefix="/case-studies"
    )

    talisker.requests.configure(cs.session)

    init_handler(app)
    init_blueprint(app)
    init_dashboard(app)

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

    @app.context_processor
    def utility_processor():
        return {"image": image_template}

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

    @app.errorhandler(410)
    def gone(error):
        """
        For 410 pages, display the 410.html template,
        passing through the error.
        """

        return flask.render_template("410.html", error=error), 410


def init_blueprint(app):
    app.register_blueprint(jaasai)
    app.register_blueprint(jaasredirects)
    app.register_blueprint(jaasstore)


def init_dashboard(app):
    """
    Add views for the dashboard
    """

    @app.route("/models")
    @app.route("/models/<path:path>")
    @app.route("/controllers")
    @app.route("/controllers/<path:path>")
    def dashboard_index(path=None):
        """
        Send /models and /controllers to the index page
        """

        return flask.render_template("dashboard/index.html")

    @app.route("/config.js")
    @app.route("/manifest.json")
    @app.route("/ghost-bundle.svg")
    def dashboard_files():
        """
        Load dashboard files directly
        """

        return flask.render_template("dashboard" + flask.request.path)
