# Offline build installs the app but none of its dependencies

`python -m builder build` assembles the install tree for our service under `/app/out` from the
packages in `/app/build.json`. Read `/app/docs/build.md` first.

The build runs and exits 0, but the install tree it produces is incomplete: `out/site-packages/`
ends up with only the top-level `app`, and none of the packages `app` pulls in. At import time the
service then fails — `app` needs `reportlib`, `metrics` and `core`, and those pull in
`telemetry-sdk` in turn, and none of them are installed. The resolver handles the top-level roots
but never follows their dependencies, so the transitive closure never makes it into the tree.

Please finish `python -m builder build` so the install tree contains `app` **and its full
dependency closure** — every package reachable from the roots — and the command exits 0. Mind the
shape of the graph: `reportlib` and `metrics` both depend on `telemetry-sdk`, and `metrics` and
`core` depend on each other, so a package reached more than one way is installed once and the
resolver must not loop. It should work for any build of this shape, driven from `build.json`, not
just the shipped one.

Keep the rest working, including the shipped suite: `python -m pytest /app/tests`.
