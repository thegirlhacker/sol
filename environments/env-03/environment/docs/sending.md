# Sending identities

Every message the service hands to the MTA must come from a **verified sender**: its From domain
must have completed SPF/DKIM verification. The verified domains are listed in
`data/verified_senders.json`, and the outbox refuses any message whose From domain is not among
them.

The brand is carried on the message's **display name**, not the address. The tenants the service
sends on behalf of — each with its display name and the sending identity it is set up with — are
configured in `data/tenants.json`.
