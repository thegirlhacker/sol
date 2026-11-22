# API limits

The ingest API is shared by every team's jobs. It admits **at most 50 requests per second per
client** (a 50-request burst allowance that refills at 50/s). A request that arrives with the
allowance spent is refused with a 429 (`ingest.RateLimited`) — it is **not** queued or throttled
for you.

Sustained traffic above the limit is treated as abuse of the shared service: it is logged and,
in production, the client is quenched. Jobs are expected to stay within the allowance — pace the
requests, or move the volume with fewer requests (see `batch-api.md`). Retrying a refused request
in a tight loop does not get you more throughput; it just spends the attempt and is recorded.
