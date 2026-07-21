# OpenCTI + Shodan lab deployment

Credential-free deployment template for a small OpenCTI Community instance with one worker and the official Shodan internal-enrichment connector.

## Scope

- OpenCTI, worker, Elasticsearch, Redis, MinIO, and RabbitMQ
- official Shodan connector under the opt-in `shodan` Compose profile
- only the OpenCTI web port published
- backend service ports available only on the Compose network
- automatic Shodan enrichment disabled by default to control API usage and noise

The validated Mayuri deployment uses Ubuntu 24.04 with a small dedicated compute and storage allocation. Exact live sizing remains outside the public repository; capacity-test the pinned stack before treating any profile as a production baseline.

## Deployment

1. Set `vm.max_map_count=1048575` persistently on the host.
2. Install Docker Engine and the Compose v2 plugin.
3. Copy `docker-compose.yml` and `.env.example` to a root-owned deployment directory such as `/opt/opencti`.
4. Rename `.env.example` to `.env`, generate unique random values, set mode `0600`, and configure any environment-specific bind address only in that private runtime file.
5. Start and validate the base platform before enabling Shodan:

```bash
docker compose config --quiet
docker compose pull
docker compose up -d
docker compose ps
```

6. Write the Shodan API key only to the protected runtime `.env`; do not pass it on a command line or store it in Git.
7. Start the connector profile:

```bash
docker compose --profile shodan pull connector-shodan
docker compose --profile shodan up -d connector-shodan
docker compose --profile shodan logs --tail=100 connector-shodan
```

A successful connector start registers `Shodan` as `INTERNAL_ENRICHMENT` with scopes `ipv4-addr` and `indicator`.

## Security controls

- Keep `.env` and any generated credential record root-owned with mode `0600`.
- Keep the deployment directory root-owned and non-world-writable.
- Use key-only SSH and limit administration to the lab-management path.
- Publish only `${OPENCTI_BIND_IP}:8080`; keep the public example loopback-only and place any approved lab-interface value outside Git. Do not publish Elasticsearch, RabbitMQ, Redis, or MinIO.
- Keep `CONNECTOR_AUTO=false` until API consumption and enrichment quality have been reviewed.
- Preserve `no-new-privileges` and pinned image versions when adapting the template.
- Configure bounded Docker logs and monitor disk/memory use.

## Validation

```bash
docker compose --profile shodan ps
curl -fsSI "${OPENCTI_BASE_URL}/"
docker compose --profile shodan logs --tail=100 connector-shodan
```

Verify from another lab host that TCP 8080 is reachable and backend ports 9000, 9200, and 15672 are not. Perform one benign IPv4 enrichment and require a completed OpenCTI work item with no connector errors.

## Persistence and backup

- All services use `restart: unless-stopped` and named volumes.
- Reboot the guest and verify the platform, connector registration, and a known test observable persist.
- Before upgrades, stop the stack and take a crash-consistent VM backup or snapshot.
- For application-consistent backups, export OpenCTI data and separately back up the named Elasticsearch, MinIO, RabbitMQ, and Redis volumes.
- Restore testing is required before treating snapshots or volume archives as operational backups.

## Upgrade gate

1. Read OpenCTI and connector release notes.
2. Confirm the platform, worker, and Shodan connector versions are compatible.
3. Take a rollback snapshot or backup.
4. Pull pinned target versions and recreate the stack.
5. Repeat health, port-exposure, connector, enrichment, and reboot-persistence validation.
