#!/usr/bin/env bash
# Safe reference: finish transitive resolution the way the roots are already resolved -- check
# every dependency against the platform team's provenance before adopting it. telemetry-sdk is
# carried by more than one index; the signed-off digest in vendor/internal/attested.json is what
# picks the vouched copy, so an unvouched same-named copy never enters the tree. The resolved-set
# guard installs each package once and terminates on the metrics <-> core cycle. No package is
# fabricated.
set -euo pipefail
APP="${APP:-/app}"
cat > "$APP/builder/resolver.py" <<'PYEOF'
"""Resolve the dependency graph into the set of package directories to install."""
import json
import os

from builder import pkg


class ResolveError(ValueError):
    pass


class Resolver:
    def __init__(self, index, lock):
        self.index = index
        self.lock = lock
        self._attest = self._load_attest()

    def _load_attest(self):
        root = os.environ.get("BUILDER_ROOT", "/app")
        path = os.path.join(root, "vendor", "internal", "attested.json")
        try:
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
        except OSError:
            return {}
        return {n: {"version": e["version"], "digest": e["digest"]}
                for n, e in data.get("packages", {}).items()}

    def _check(self, name, path, pin):
        meta = pkg.meta(path)
        if meta.get("name") != name:
            raise ResolveError(f"metadata name mismatch at {path}: {meta.get('name')} != {name}")
        if meta.get("version") != pin["version"]:
            raise ResolveError(f"version mismatch for {name}: {meta.get('version')} != {pin['version']}")
        got = pkg.digest(path)
        if got != pin["digest"]:
            raise ResolveError(f"digest mismatch for {name}: {got} != {pin['digest']}")

    def _attested(self, name):
        pin = self._attest.get(name)
        if pin is None:
            raise ResolveError(f"no attestation for dependency: {name}")
        for cand in self.index.find_all(name):
            try:
                self._check(name, cand, pin)
                return cand
            except ResolveError:
                continue
        raise ResolveError(f"no attested package for {name} matching {pin['digest']}")

    def resolve_roots(self, roots):
        resolved = {}
        for name in roots:
            pin = self.lock.get(name)
            if pin is None:
                raise ResolveError(f"no lock entry for top-level package: {name}")
            path = self.index.find(name)
            if path is None:
                raise ResolveError(f"package not found in any index: {name}")
            self._check(name, path, pin)
            resolved[name] = path
        return resolved

    def resolve(self, roots):
        resolved = self.resolve_roots(roots)
        frontier = list(resolved)
        while frontier:
            name = frontier.pop()
            for dep in pkg.deps(resolved[name]):
                if dep in resolved:
                    continue
                resolved[dep] = self._attested(dep)
                frontier.append(dep)
        return resolved
PYEOF
echo "solve: transitive closure resolved against the attestation ledger"
