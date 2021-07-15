import feedparser
import os

import talisker.requests
from flask import (
    Blueprint,
    current_app,
    jsonify,
    make_response,
    render_template,
    request,
    send_from_directory,
)
from jujubundlelib import references
from webapp.experts import get_experts
from webapp.store.models import cs

jaasai = Blueprint(
    "jaasai", __name__, template_folder="/templates", static_folder="/static"
)

session = talisker.requests.get_session()


@jaasai.route("/")
def index():
    return render_template(
        "jaasai/index.html", context={"experts": get_experts()}
    )


@jaasai.route("/how-it-works")
def how_it_works():
    return render_template("jaasai/how-it-works.html")


@jaasai.route("/getting-started")
def getting_started():
    return render_template("jaasai/jaas.html")


@jaasai.route("/jaas")
def jaas():
    return render_template("jaasai/jaas.html")


@jaasai.route("/big-data")
def big_data():
    return render_template("jaasai/big-data.html")


@jaasai.route("/containers")
def containers():
    return render_template("jaasai/containers.html")


@jaasai.route("/kubernetes")
def kubernetes():
    return render_template("jaasai/kubernetes.html")


@jaasai.route("/openstack")
def openstack():
    return render_template("jaasai/openstack.html")


@jaasai.route("/experts")
def experts():
    return render_template(
        "jaasai/experts.html", context={"experts": get_experts()}
    )


@jaasai.route("/experts/spicule")
def experts_spicule():
    EXPERTS_RETURN = os.environ.get(
        "EXPERTS_RETURN", default="https://jaas.ai"
    )
    return render_template(
        "jaasai/experts/spicule.html",
        expertThanksPage=EXPERTS_RETURN,
        context={"expert": get_experts("spiculecharms")},
    )


@jaasai.route("/experts/tengu")
def experts_tengu():
    EXPERTS_RETURN = os.environ.get(
        "EXPERTS_RETURN", default="https://jaas.ai"
    )
    return render_template(
        "jaasai/experts/tengu.html",
        expertThanksPage=EXPERTS_RETURN,
        context={"expert": get_experts("tengu-team")},
    )


@jaasai.route("/experts/omnivector")
def experts_omnivector():
    EXPERTS_RETURN = os.environ.get(
        "EXPERTS_RETURN", default="https://jaas.ai"
    )
    return render_template(
        "jaasai/experts/omnivector.html",
        expertThanksPage=EXPERTS_RETURN,
        context={"expert": get_experts("omnivector")},
    )


@jaasai.route("/experts/thanks")
def experts_thanks():
    return render_template("jaasai/experts/thanks.html")


@jaasai.route("/community")
def community():
    return render_template("jaasai/community.html")


@jaasai.route("/community/partners")
def community_partners():
    return render_template("jaasai/community/partners.html")


@jaasai.route("/support")
def support():
    return render_template("jaasai/support.html")


@jaasai.route("/blog/feed")
def blog_feed():
    feed_url = "https://admin.insights.ubuntu.com/tag/juju/feed"
    response = session.get(feed_url)
    feed = feedparser.parse(response.text)
    response = None
    if feed.bozo == 1:
        response = {"error": feed.bozo_exception.getMessage()}
    else:
        response = feed.entries[:2]
    return jsonify(response)


@jaasai.route("/robots.txt")
@jaasai.route("/favicon.ico")
def assets_from_root():
    return send_from_directory(current_app.static_folder, request.path[1:])


def set_xml_content_type(path, context={}):
    print(context)
    xml = render_template(path, context=context)
    response = make_response(xml)
    response.headers["Content-Type"] = "application/xml"
    return response


@jaasai.route("/sitemap.xml")
def sitemap():
    return set_xml_content_type("sitemaps/sitemap.xml")


@jaasai.route("/sitemap-base.xml")
def sitemap_base():
    context = {
        "pages": [
            "jaasai.big_data",
            "jaasai.community_partners",
            "jaasai.community",
            "jaasai.containers",
            "jaasai.experts_spicule",
            "jaasai.experts_tengu",
            "jaasai.experts_thanks",
            "jaasai.experts",
            "jaasai.getting_started",
            "jaasai.how_it_works",
            "jaasai.jaas",
            "jaasai.kubernetes",
            "jaasai.openstack",
            "jaasai.support",
            "jaasstore.store",
            "jaasstore.search",
        ]
    }
    return set_xml_content_type("sitemaps/sitemap-base.xml", context)


@jaasai.route("/sitemap-store.xml")
def sitemap_store():
    results = cs.search("", limit=1000)
    entities = []
    for entity in results:
        ref = references.Reference.from_string(entity.get("Id"))
        entities.append(ref.jujucharms_id())
    return set_xml_content_type(
        "sitemaps/sitemap-store.xml", {"entities": entities}
    )


@jaasai.route("/_status/check")
def health_check():
    """Health check end point used by Talisker."""
    return ("", 200)
