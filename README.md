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

## Discovery API Notes

```sh
# Create env
curl -X POST -u "apikey:{apiKey}" \
    -H "Content-Type: application/json" \
    -d "{\"name\":\"{envName}\", \"description\":\"{envDescription}\"}" \
    "{url}/v1/environments?version=2018-12-03"

# Check env status
curl -u "apikey:{apiKey}" \
    "{url}/v1/environments/{envId}?version=2018-12-03"

# Get env default collection id
curl -u "apikey:{apikey}" \
    "{url}/v1/environments/{environment_id}/configurations?version=2018-12-03"

# Create collection
curl -X POST -u "apikey:{apikey}" \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"my-first-collection\", \"description\": \"exploring collections\", \"configuration_id\":\"{configuration_id}\" , \"language": \"en_us\"}" \
    "{url}/v1/environments/{environment_id}/collections?version=2018-12-03"

# Check collection status
curl -u "apikey:{apikey}" \
    "{url}/v1/environments/{environment_id}/collections/{collection_id}?version=2018-12-03"
```
