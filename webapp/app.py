import flask
import datetime

import talisker
from canonicalwebteam.flask_base.app import FlaskBase
from canonicalwebteam.yaml_responses.flask_helpers import (
    prepare_deleted,
    prepare_redirects,
)
from canonicalwebteam import image_template

from webapp.handlers import add_headers
from webapp.jaasai.views import jaasai
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
    app.before_request(prepare_redirects("redirects.yaml"))
    app.before_request(
        prepare_redirects("permanent-redirects.yaml", permanent=True)
    )
    app.before_request(prepare_deleted())

    # Handlers
    # ===
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

    # Blueprints
    # ===
    app.register_blueprint(jaasai)

    @app.route("/q/")
    @app.route("/q/<path:path>")
    def search_redirect(path=None):
        """
        Handle redirects from jujucharms.com search URLS to the jaas.ai format.
        e.g. /q/k8s/demo?sort=-name&series=xenial will redirect to
        /search?q=k8s+demo&sort=-name&series=xenial
        """
        query_string = []
        if path:
            query_string.append("q={}".format(path.replace("/", "+")))
        if flask.request.query_string:
            query_string.append(str(flask.request.query_string, "utf-8"))
        return flask.redirect(
            "/search?{}".format("&".join(query_string)), code=302
        )

    @app.route("/<charm_or_bundle_name>")
    @app.route("/<charm_or_bundle_name>/<series_or_version>")
    @app.route("/<charm_or_bundle_name>/<series_or_version>/<version>")
    def details_redirect(
        charm_or_bundle_name,
        series_or_version=None,
        version=None,
    ):
        charmhub_url = "https://charmhub.io/" + charm_or_bundle_name
        return flask.redirect(charmhub_url, code=301)

    # Template filters
    # ===
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


app = create_app()
