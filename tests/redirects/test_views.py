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
