from flask import Blueprint, redirect, request

from webapp.external_urls import external_urls


jaasredirects = Blueprint(
    "jaasredirects",
    __name__,
    template_folder="/templates",
    static_folder="/static",
)


@jaasredirects.route("/q/")
@jaasredirects.route("/q/<path:path>")
def search_redirect(path=None):
    """
    Handle redirects from jujucharms.com search URLS to the jaas.ai format.
    e.g. /q/k8s/demo?sort=-name&series=xenial will redirect to
    /search?q=k8s+demo&sort=-name&series=xenial
    """
    query_string = []
    if path:
        query_string.append("q={}".format(path.replace("/", "+")))
    if request.query_string:
        query_string.append(str(request.query_string, "utf-8"))
    return redirect("/search?{}".format("&".join(query_string)), code=302)


@jaasredirects.route("/blog")
def blog_redirect():
    """
    Redirect the blog page that existed on jujucharms.com.
    """
    return redirect(external_urls["blog"], code=302)


@jaasredirects.route("/big-data")
def big_data_redirect():
    charmhub_url = "https://charmhub.io/?base=all&filter=big-data"
    return redirect(charmhub_url, code=301)


@jaasredirects.route("/containers")
def containers_redirect():
    charmhub_url = "https://charmhub.io/?base=all&filter=containers"
    return redirect(charmhub_url, code=301)


@jaasredirects.route("/kubernetes")
def kubernetes_redirect():
    charmhub_url = "https://charmhub.io/?base=kubernetes"
    return redirect(charmhub_url, code=301)


@jaasredirects.route("/openstack")
def openstack_redirect():
    charmhub_url = "https://charmhub.io/?base=linux"
    return redirect(charmhub_url, code=301)
