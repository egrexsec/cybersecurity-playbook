# OpenCTI + Shodan live validation — 2026-07-20

## Scope

Sanitized validation record for the Mayuri lab CTI server. Secret values and administrative credentials are intentionally excluded.

## Platform

- Proxmox VM: `170`
- guest hostname: `mayuri-osint`
- lab address: `10.10.10.50`
- guest OS: Ubuntu 24.04 LTS
- capacity: 4 vCPU, 10 GiB fixed RAM, 80 GB virtual disk
- OpenCTI platform/worker: `7.260715.0`
- Shodan connector: `7.260715.0`
- Elasticsearch: `8.19.16`
- Redis: `8.8.0`
- RabbitMQ: `4.3-management`
- MinIO: `RELEASE.2025-09-07T16-13-09Z`

## Security checks

- OpenCTI is bound to `10.10.10.50:8080` on the isolated lab bridge.
- Elasticsearch `9200`, MinIO `9000`, and RabbitMQ management `15672` were unreachable from the Mayuri bridge.
- Runtime environment and generated administrative credential files were root-owned with mode `0600`.
- The deployment directory was root-owned with mode `0750`; Compose was mode `0640`.
- SSH effective policy: key authentication enabled; password, keyboard-interactive, and root login disabled; login restricted to the installed administrative user.
- Docker uses bounded local logging.
- OpenCTI telemetry is disabled.
- Shodan automatic enrichment is disabled; enrichment is analyst-triggered.

## Functional validation

1. The Shodan API credential was supplied through guest-agent stdin and written directly to the protected runtime environment.
2. The credential passed the Shodan API account check; its value was not printed or committed.
3. OpenCTI reported the Shodan connector as active `INTERNAL_ENRICHMENT` with scopes `ipv4-addr` and `indicator`.
4. A benign IPv4 observable for `1.1.1.1` was created for deployment validation.
5. OpenCTI queued enrichment through the registered Shodan connector.
6. The connector acknowledged the message, read the observable, submitted a STIX bundle, and reported the work processed.
7. The work completed with zero errors and 27 processing expectations.

## Reboot persistence

After a full guest reboot:

- QEMU guest agent returned successfully;
- Docker and QEMU guest agent were active;
- OpenCTI and all four dependency services returned healthy;
- the worker and Shodan connector returned running;
- the OpenCTI UI returned HTTP 200;
- the `1.1.1.1` observable remained present;
- backend ports remained unexposed.

- All services returned through `restart: unless-stopped` after a full guest reboot.
- A clean application-stopped Proxmox snapshot, `opencti-shodan-validated-20260720`, was created after validation and the stack was returned to healthy service.

Observed after reboot:

- memory: approximately 3.9 GiB used, 5.8 GiB available, no swap consumed;
- root filesystem: approximately 12 GiB used of 76 GiB usable.

## Result

**PASS** — the pinned OpenCTI stack and official Shodan connector are operational, credential-protected, network-minimized, enrichment-tested, and persistent across guest reboot.

## Limitations

- Access is currently HTTP on the isolated lab network; no public exposure or reverse proxy is part of this validation.
- A clean post-validation Proxmox snapshot exists, but application-consistent export/volume backup and restore testing remains a separate operational task.
- The benign validation observable is retained as reproducible evidence and may be removed after documentation review.
