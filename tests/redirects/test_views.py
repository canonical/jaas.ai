from flask import url_for
from flask_testing import TestCase
from unittest.mock import patch

from webapp.app import create_app


class RedirectViews(TestCase):
    render_templates = False

    def create_app(self):
        app = create_app(testing=True)
        app.config["PRESERVE_CONTEXT_ON_EXCEPTION"] = False
        return app

    def test_redirect_logo(self):
        response = self.client.get("/static/img/logos/juju-logo.svg")
        self.assertEqual(response.status_code, 301)
        self.assertEqual(
            response.location,
            "https://assets.ubuntu.com/v1/7e21b535-logo-juju.svg",
        )

    @patch("webapp.store.models.search_entities")
    def test_search_redirect(self, mock_search_entities):
        mock_search_entities.return_value = []
        response = self.client.get("/q/k8s")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.location,
            "http://localhost{}".format(url_for("jaasstore.search", q="k8s")),
        )

    @patch("webapp.store.models.search_entities")
    def test_search_redirect_multi_word(self, mock_search_entities):
        mock_search_entities.return_value = []
        response = self.client.get("/q/k8s/demo")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.location,
            "http://localhost{}".format(
                url_for("jaasstore.search", q="k8s demo")
            ),
        )

    @patch("webapp.store.models.search_entities")
    def test_search_redirect_query_params(self, mock_search_entities):
        mock_search_entities.return_value = []
        response = self.client.get("/q/k8s?sort=name&series=xenial")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.location,
            "http://localhost{}".format(
                url_for(
                    "jaasstore.search", q="k8s", sort="name", series="xenial"
                )
            ),
        )

    @patch("webapp.store.models.search_entities")
    def test_search_redirect_just_query_params(self, mock_search_entities):
        mock_search_entities.return_value = []
        response = self.client.get("/q?tags=proxy")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.location,
            "http://localhost{}".format(
                url_for("jaasstore.search", tags="proxy")
            ),
        )
