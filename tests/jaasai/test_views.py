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
            "/",
            "/big-data",
            "/community",
            "/community/cards",
            "/community/charmers",
            "/community/partners",
            "/containers",
            "/experts",
            "/experts/spicule",
            "/experts/tengu",
            "/experts/thanks",
            "/getting-started",
            "/how-it-works",
            "/jaas",
            "/kubernetes",
            "/openstack",
        ]
        for page in pages:
            response = self.client.get(page)
            self.assertEqual(
                response.status_code, 200, "For page: {}".format(page)
            )
