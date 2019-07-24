import flask

from canonicalwebteam.discourse_docs import (
    DiscourseAPI,
    DiscourseDocs,
    DocParser,
)

from canonicalwebteam.search import build_search_view


def init_docs(app, url_prefix):
    discourse_index_id = 1868

    discourse_api = DiscourseAPI(base_url="https://discourse.jujucharms.com/")
    discourse_parser = DocParser(discourse_api, discourse_index_id, url_prefix)
    discourse_docs = DiscourseDocs(
        parser=discourse_parser,
        category_id=22,
        document_template="docs/document.html",
        url_prefix=url_prefix,
    )

    discourse_docs.init_app(app)

    # Remove homepage route so we can redefine it
    for url in app.url_map._rules:
        if url.rule == url_prefix + "/":
            app.url_map._rules.remove(url)

    @app.route(url_prefix)
    def homepage():
        """
        Show the custom homepage
        """
        discourse_parser.parse()

        return flask.render_template(
            "docs/homepage.html", navigation=discourse_parser.navigation
        )

    @app.route(url_prefix + "/commands")
    def commands():
        """
        Show the static commands page
        """

        discourse_parser.parse()

        return flask.render_template(
            "docs/commands.html", navigation=discourse_parser.navigation
        )

    app.add_url_rule(
        "/docs/search",
        "docs-search",
        build_search_view(
            site="docs.jujucharms.com", template_path="docs/search.html"
        ),
    )
