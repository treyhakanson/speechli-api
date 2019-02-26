[![Build Status](https://travis-ci.com/treyhakanson/speechli-api.svg?branch=master)](https://travis-ci.com/treyhakanson/speechli-api)

# Speechli API

Install [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/install/) before continuing.

To run:

```sh
docker-compose up -d
```

To stop:

```sh
docker-compose down
```

To rebuild the project:

```sh
docker-compose build
```

## Utilities

To perform a bulk document upload to the Watson Discovery collection (can pass either a directory or a file):

```sh
docker-compose run --rm -v <path/to/data>:/tmp/data speechli-api \
    python discovery.py /tmp/data
```

For example, if you have data locally at `/path/to/dir` and `/path/to/file.json` (note that this _must_ be an absolute path):

```sh
# If a directory
docker-compose run --rm -v /path/to/dir:/tmp/data speechli-api \
    python discovery.py /tmp/data

# If a file
docker-compose run --rm -v /path/to/file.json:/tmp/data/file.json speechli-api \
    python discovery.py /tmp/data/file.json
```

Note that the upload process is relatively slow.
