from flask import url_for


def get_experts(expert=None):
    """Generate the expert definitions. This needs to be done in a function so
        that it can be called when the app context is available. This is so
        that the url_for methods work.
        :param expert: A optional expert. If provided this method will only
            return that expert.
        :returns: One or all experts.
    """
    experts = {
        "spiculecharms": {
            "name": "Spicule",
            "logo": url_for("static", filename="img/logos/spicule.png"),
            "highlights": [
                "Machine learning",
                "Data service deployments",
                "Container orchestration",
            ],
            "contactDescription": (
                "Please let us know if you have a question, or would like further "
                "information about Spicule."
            ),
            "website": "www.spicule.co.uk",
            "email": "juju-partners@spicule.co.uk",
            "phoneNumbers": ["UK +44 (0)1603 327762", "US +1 8448141689"],
            "store_card": {
                "heading": "Spicule&rsquo;s solutions can solve your Big Data challenge.",
                "button_view": "jaasai.experts_spicule",
                "button_label": "Big data experts",
            },
        },
        "tengu-team": {
            "name": "Tengu",
            "logo": url_for("static", filename="img/logos/tengu.png"),
            "highlights": [
                "Your own Big Data workspace",
                "Use all Juju-charmed technologies",
                "Machine Learning, IoT, Microservices",
            ],
            "contactDescription": (
                "Please let us know if you have a question, or would like further "
                "information about Tengu."
            ),
            "website": "https://tengu.io",
            "email": "info@tengu.io",
            "phoneNumbers": ["BE +32 478 66 84 89"],
            "store_card": {
                "heading": "Spicule&rsquo;s solutions can solve your Big Data challenge.",
                "button_view": "jaasai.experts_spicule",
                "button_label": "Big data experts",
            },
        },
    }
    if expert:
        return experts.get(expert)
    else:
        return experts
