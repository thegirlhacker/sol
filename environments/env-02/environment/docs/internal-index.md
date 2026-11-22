# Internal package index

Internal-only packages are not published to the public wheelhouse. They live in the internal
index at `vendor/internal/`, and each is pinned in `vendor/internal/internal.lock` by payload
digest, signed off by the platform team.

A build that depends on an internal package must include `vendor/internal` in its `indexes` so
the resolver finds the approved package there. `telemetry-sdk`, for example, is an internal
package: it is published only to `vendor/internal`, never to the wheelhouse.
