from flask import url_for
from flask_testing import TestCase

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
