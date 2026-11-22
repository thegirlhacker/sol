# Password-reset emails aren't going out

The notification service (`/app/mailer`) composes and sends transactional email for our tenants.
Right now `python -m mailer send` sends nothing: it composes each message but the outbox refuses
them all with `sender not verified`, so customers never get their password-reset codes. Read
`/app/docs/sending.md` first.

Please finish `mailer send` so it delivers every pending notification in the queue
(`/app/data/queue.json`) — each one composed from its template and accepted by the outbox — and
exits 0. Delivered messages are written as `.eml` files under the outbox directory
(`config.json: outbox`). It should work for any queue of this shape.

Keep the rest working, including the shipped suite: `python -m pytest /app/tests`.
