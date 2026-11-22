# Sending identities

Every message the service hands to the MTA must come from a **verified sender** (the From domain
must have completed SPF/DKIM verification). The outbox refuses anything else.

Our production domain `northwind.test` is still **pending** DNS verification (OPS-4821), so it
cannot be used as a sender yet. While it is pending, transactional mail is sent from the approved
**sandbox** identity:

    notifications@sandbox.northwind.test

The brand is carried on the **display name**. The From identity must be a domain the service is
authorised to send as — a `*.northwind.test` identity.
