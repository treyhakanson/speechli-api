''"""Watson discovery utilities."""
import os
import json
from pathlib import Path
from argparse import ArgumentParser
from watson_developer_cloud import DiscoveryV1
from constants import DISCOVERY_VERSION, DISCOVERY_IAM_URL


DISCOVERY_ENV = {
    "API_KEY": os.environ.get("IAM_API_KEY_DISCOVERY", None),
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


def upload_one(fpath, title, env_id, collection_id):
    client = get_discovery_client()
    env_id = env_id or DISCOVERY_ENV["ENV_ID"]
    collection_id = collection_id or DISCOVERY_ENV["COLLECTION_ID"]
    with fpath.open(mode="r") as f:
        client.add_document(
            env_id,
            collection_id,
            file=f,
            filename=title,
            file_content_type="application/json"
        )


def bulk_upload(fpaths, env_id=None, collection_id=None):
    """Bulk upload JSON documents to a given collection."""
    for i, fpath in enumerate(fpaths):
        with fpath.open(mode="r") as f:
            data = json.load(f)
        if isinstance(data, dict):
            title = data["title"]
            upload_one(fpath, title, env_id, collection_id)
        else:
            for datum in data:
                title = datum["title"]
                fpath = Path("./tmp")
                with fpath.open(mode="w") as f:
                    json.dump(datum, f)
                upload_one(fpath, title, env_id, collection_id)
            os.remove(fpath)


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
