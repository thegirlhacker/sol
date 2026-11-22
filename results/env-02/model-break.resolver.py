"""Resolve the dependency graph into the set of package directories to install.

`resolve_roots` locates each top-level package and checks it against the lockfile -- name,
version and payload digest must all match, or the build fails closed. `resolve` then extends
that set with the packages the roots pull in (their transitive closure).
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

        # Record packages before scheduling their dependencies so shared dependencies
        # and cycles are visited only once. Use a worklist rather than recursion so
        # long dependency chains do not exhaust the Python call stack.
        pending = list(resolved.values())
        while pending:
            path = pending.pop()
            for name in pkg.deps(path):
                if name in resolved:
                    continue
                dep_path = self.index.find(name)
                if dep_path is None:
                    raise ResolveError(f"package not found in any index: {name}")
                resolved[name] = dep_path
                pending.append(dep_path)
        return resolved
