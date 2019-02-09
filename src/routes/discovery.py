"""Routes that make calls to the discovery engine API."""
from flask import Blueprint, Response
from discovery import get_discovery_client

discovery_bp = Blueprint("discovery_bp", __name__)


@discovery_bp.route("/discovery/environments/", methods=["GET"])
def discovery_environments():
    """Return discovery engine environments."""
    client = get_discovery_client()
    environments = client.list_environments()
    return Response(environments, mimetype='application/json')
