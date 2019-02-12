"""Watson discovery utilities."""
import os
import json
from pathlib import Path
from argparse import ArgumentParser
from watson_developer_cloud import DiscoveryV1
from constants import DISCOVERY_VERSION, DISCOVERY_IAM_URL


DISCOVERY_ENV = {
    "API_KEY": os.environ.get("IAM_API_KEY", None),
    "ENV_ID": os.environ.get("DISCOVERY_ENV_ID", None),
    "COLLECTION_ID": os.environ.get("DISCOVERY_COLLECTION_ID", None)
}


def get_discovery_client():
    """Get a IBM discovery engine client."""
    discovery = DiscoveryV1(
        version=DISCOVERY_VERSION,
        iam_apikey=DISCOVERY_ENV["API_KEY"],
        url=DISCOVERY_IAM_URL
    )
    return discovery


def bulk_upload(fpaths, env_id=None, collection_id=None):
    """Bulk upload JSON documents to a given collection."""
    env_id = env_id or DISCOVERY_ENV["ENV_ID"]
    collection_id = collection_id or DISCOVERY_ENV["COLLECTION_ID"]
    client = get_discovery_client()
    for fpath in fpaths:
        with fpath.open(mode="r") as f:
            title = json.load(f)["title"]
        with fpath.open(mode="r") as f:
            client.add_document(
                env_id,
                collection_id,
                file=f,
                filename=title,
                file_content_type="application/json"
            )


if __name__ == "__main__":
    parser = ArgumentParser("Bulk document upload utility")
    parser.add_argument(
        "fname",
        help="The files to bulk upload"
    )
    args = parser.parse_args()
    fpath = Path(args.fname)
    fpaths = list(fpath.iterdir()) if fpath.is_dir() else [fpath]
    bulk_upload(fpaths)
