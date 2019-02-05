"""Routes that make calls to the discovery engine API."""
import os
from flask import Blueprint, Response
from watson_developer_cloud import DiscoveryV1
from constants import DISCOVERY_VERSION, DISCOVERY_URL

discovery_bp = Blueprint("discovery_bp", __name__)


def get_discovery_client():
    """Get a IBM discovery engine client."""
    discovery = DiscoveryV1(
        version=DISCOVERY_VERSION,
        iam_apikey=os.getenv("IAM_API_KEY"),
        url=DISCOVERY_URL
    )
    return discovery


@discovery_bp.route("/discovery/environments/", methods=["GET"])
def discovery_environments():
    """Return discovery engine environments."""
    client = get_discovery_client()
    environemnts = client.list_environments()
    return Response(environemnts, mimetype='application/json')
