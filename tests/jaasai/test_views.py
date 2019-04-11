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
            "big_data",
            "community_cards",
            "community_partners",
            "community",
            "containers",
            "experts_spicule",
            "experts_tengu",
            "experts_thanks",
            "experts",
            "getting_started",
            "how_it_works",
            "index",
            "jaas",
            "kubernetes",
            "openstack",
            "support",
        ]
        for page in pages:
            url = url_for("jaasai.{}".format(page))
            response = self.client.get(url)
            self.assertEqual(
                response.status_code, 200, "For page: {}".format(url)
            )

    @patch("feedparser.parse")
    def test_blog_feed(self, mock_parse):
        mock_parse.return_value = MagicMock(
            bozo=0, entries=[{"title": "A blog post"}]
        )
        response = self.client.get(url_for("jaasai.blog_feed"))
        self.assertEqual(
            response.data, b'[\n  {\n    "title": "A blog post"\n  }\n]\n'
        )

    @patch("feedparser.parse")
    def test_blog_feed_only_5(self, mock_parse):
        mock_parse.return_value = MagicMock(
            bozo=0,
            entries=[
                {"title": 1},
                {"title": 2},
                {"title": 3},
                {"title": 4},
                {"title": 5},
                {"title": 6},
            ],
        )
        response = self.client.get(url_for("jaasai.blog_feed"))
        self.assertEqual(len(json.loads(response.data)), 2)

    @patch("feedparser.parse")
    def test_blog_feed_invalid(self, mock_parse):
        feed = MagicMock(
            bozo=1,
            bozo_exception=MagicMock(
                getMessage=MagicMock(return_value="Syntax error")
            ),
        )
        mock_parse.return_value = feed
        response = self.client.get(url_for("jaasai.blog_feed"))
        self.assertEqual(response.data, b'{\n  "error": "Syntax error"\n}\n')
