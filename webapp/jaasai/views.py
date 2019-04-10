from flask import Blueprint, render_template
import os

jaasai = Blueprint(
    "jaasai", __name__, template_folder="/templates", static_folder="/static"
)


@jaasai.route("/")
def index():
    return render_template("jaasai/index.html")


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
    return render_template("jaasai/experts.html")


@jaasai.route("/experts/spicule")
def experts_spicule():
    EXPERTS_RETURN = os.environ.get(
        "EXPERTS_RETURN", default="https://jaas.ai"
    )
    return render_template(
        "jaasai/experts/spicule.html", expertThanksPage=EXPERTS_RETURN
    )


@jaasai.route("/experts/tengu")
def experts_tengu():
    return render_template("jaasai/experts/tengu.html")


@jaasai.route("/experts/thanks")
def experts_thanks():
    return render_template("jaasai/experts/thanks.html")


@jaasai.route("/community")
def community():
    return render_template("jaasai/community.html")


@jaasai.route("/community/cards")
def community_cards():
    return render_template("jaasai/community/cards.html")


@jaasai.route("/community/partners")
def community_partners():
    return render_template("jaasai/community/partners.html")


@jaasai.route("/support")
def support():
    return render_template("jaasai/support.html")


@jaasai.route("/_status/check")
def health_check():
    """ Health check end point used by Talisker.
    """
    return ("", 200)
