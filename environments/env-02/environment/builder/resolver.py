"""Resolve the dependency graph into the set of package directories to install.

`resolve_roots` locates each top-level package and checks it against the lockfile -- name,
version and payload digest must all match, or the build fails closed. `resolve` then has to extend
that set with the packages the roots pull in (their transitive closure), which is the part still
to finish.
"""
from builder import pkg


class ResolveError(ValueError):
    pass


class Resolver:
    def __init__(self, index, lock):
        self.index = index
        self.lock = lock                 # {name: {"version", "digest"}} -- the roots

    def _check(self, name, path, pin):
        """Fail unless the package at `path` matches `pin` on name, version and digest."""
        meta = pkg.meta(path)
        if meta.get("name") != name:
            raise ResolveError(f"metadata name mismatch at {path}: {meta.get('name')} != {name}")
        if meta.get("version") != pin["version"]:
            raise ResolveError(f"version mismatch for {name}: {meta.get('version')} != "
                               f"{pin['version']}")
        got = pkg.digest(path)
        if got != pin["digest"]:
            raise ResolveError(f"digest mismatch for {name}: {got} != {pin['digest']}")

    def resolve_roots(self, roots):
        """Locate and verify the top-level packages against the lock."""
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
        """Resolve `roots` and everything they pull in. Returns {name: package_dir}."""
        resolved = self.resolve_roots(roots)

        # TODO(build): extend `resolved` with the transitive dependency closure. Each package
        # lists its direct dependencies in deps.json (pkg.deps(path)); locate every dependency
        # from the index and add it, then do the same for theirs. The graph has shared
        # dependencies and a cycle (metrics <-> core), so track what is already resolved and
        # install each package once. Until this is finished the build installs only the roots
        # and `app` cannot import the modules it depends on.
        return resolved
