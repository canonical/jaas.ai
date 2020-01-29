import flask

from canonicalwebteam.discourse_docs import (
    DiscourseAPI,
    DiscourseDocs,
    DocParser,
)

from canonicalwebteam.search import build_search_view


def init_docs(app, url_prefix):
    discourse_index_id = 1087

    discourse_api = DiscourseAPI(base_url="https://discourse.jujucharms.com/")
    discourse_parser = DocParser(
        discourse_api, 22, discourse_index_id, url_prefix
    )
    discourse_docs = DiscourseDocs(
        parser=discourse_parser,
        document_template="docs/document.html",
        url_prefix=url_prefix,
    )

    discourse_docs.init_app(app)

    @app.route(url_prefix + "/commands")
    def commands():
        """
        Show the static commands page
        """

        discourse_parser.parse()

        return flask.render_template(
            "docs/commands.html",
            document={"title": "Command reference"},
            navigation=discourse_parser.navigation,
        )

    app.add_url_rule(
        "/docs/search",
        "docs-search",
        build_search_view(
            site="jaas.ai/docs", template_path="docs/search.html"
        ),
    )
