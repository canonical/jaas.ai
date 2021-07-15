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

    @patch("webapp.jaasai.views.session.get")
    def test_blog_feed(self, mock_get):
        feed = "<rss><channel><item><title>Post</title></item></channel></rss>"
        mock_get.return_value = MagicMock(text=feed)
        response = self.client.get(url_for("jaasai.blog_feed"))
        posts = json.loads(response.data)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]["title"], "Post")

    @patch("webapp.jaasai.views.session.get")
    def test_blog_feed_limit_results(self, mock_get):
        feed = (
            "<rss><channel><item><title>Post</title></item>"
            "<item><title>Post</title></item>"
            "<item><title>Post</title></item></channel></rss>"
        )
        mock_get.return_value = MagicMock(text=feed)
        response = self.client.get(url_for("jaasai.blog_feed"))
        self.assertEqual(len(json.loads(response.data)), 2)

    @patch("webapp.jaasai.views.session.get")
    def test_blog_feed_invalid(self, mock_get):
        mock_get.return_value = MagicMock(text="")
        response = self.client.get(url_for("jaasai.blog_feed"))
        self.assertEqual(json.loads(response.data), [])
