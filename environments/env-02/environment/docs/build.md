# Offline builder

`python -m builder build` assembles the install tree under `out/site-packages/` from the packages
named in `build.json`:

- `roots` — the top-level packages to install. Each is pinned in `requirements.lock` by version
  and payload **digest**; `resolve_roots` locates the package and checks its name, version and
  digest against the pin, failing the build if any differ.
- `indexes` — the directories searched for a package, **in order, first match wins**
  (`Index.find`). This build searches the public `wheelhouse`, the shared `pypi-cache`, and the
  internal index under `vendor/internal`.
- `out` — where the install tree is written.

Each package is a directory with `meta.json` (name + version), an optional `deps.json` listing its
direct dependencies by name, and a `payload/` copied into `out/site-packages/<name>/`.
`pkg.digest` is the content digest a pin is checked against.

The platform team keeps `vendor/internal/attested.json` — the signed-off version and digest for
the internal supply chain — alongside the internal index.
