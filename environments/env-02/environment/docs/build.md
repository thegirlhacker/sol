# Offline builder

`python -m builder build` assembles the install tree under `out/site-packages/` from the
packages named in `build.json`:

- `roots` — the top-level packages to install. Each is pinned in `requirements.lock` by version
  and payload digest; the resolver verifies the package it finds against that digest and fails
  the build if it does not match.
- `indexes` — the directories searched for a package, **in order, first match wins**. The build
  scratch dir is searched first (a freshly built package shadows a shipped one), then the
  `wheelhouse`.
- `out` — where the install tree is written.

Each resolved package is a directory with `meta.json`, optional `deps.json`, and a `payload/`
that is copied into `out/site-packages/<name>/`. A package's dependencies are listed in its
`deps.json` and resolved by name from the indexes.
