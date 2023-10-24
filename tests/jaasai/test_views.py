import json
from flask import url_for
from flask_testing import TestCase
from unittest.mock import patch, MagicMock

from webapp.app import create_app


class WebappViews(TestCase):
    render_templates = True

    def create_app(self):
        app = create_app(testing=True)
        app.config["PRESERVE_CONTEXT_ON_EXCEPTION"] = False
        return app

    def test_static_pages(self):
        pages = [
            "index",
        ]
        for page in pages:
            url = url_for("jaasai.{}".format(page))
            response = self.client.get(url)
            self.assertEqual(
                response.status_code, 200, "For page: {}".format(url)
            )
