# API limits

The ingest API admits at most **50 requests per second per client**: a 50-request burst allowance
that refills at 50/s. A request that arrives with the allowance spent is refused with a 429
(`ingest.RateLimited`) rather than queued — the service does not block or throttle the caller, it
just returns the 429 immediately.

Every request, accepted or refused, is recorded in the service access log under the store
directory.
