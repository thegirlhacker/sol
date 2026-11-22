"""Resolve the dependency graph into a concrete set of package directories to install.

Top-level packages (the ones named in `requirements.lock`) are verified: the package found in
the index must match the digest the lock pins, or the build fails closed. Their dependencies are
read from each package's `deps.json` and resolved by name from the indexes.
"""
from builder import pkg


class ResolveError(ValueError):
    pass


class Resolver:
    def __init__(self, index, lock):
        self.index = index
        self.lock = lock              # {name: {"version","digest"}}

    def _locate(self, name):
        found = self.index.find(name)
        if found is None:
            raise ResolveError(f"package not found in any index: {name}")
        return found

    def resolve(self, roots):
        """Resolve `roots` (top-level names) and everything they pull in.

        Returns {name: package_dir}. Top-level packages are checked against the lock digest;
        dependencies are resolved by name from the indexes.
        """
        resolved = {}
        # Top-level: verified against the lock.
        for name in roots:
            path = self._locate(name)
            want = self.lock.get(name)
            if want is None:
                raise ResolveError(f"no lock entry for top-level package: {name}")
            got = pkg.digest(path)
            if got != want["digest"]:
                raise ResolveError(f"digest mismatch for {name}: {got} != {want['digest']}")
            resolved[name] = path

        # Transitive closure: resolved by name from the indexes.
        frontier = list(resolved)
        while frontier:
            name = frontier.pop()
            for dep in pkg.deps(resolved[name]):
                if dep in resolved:
                    continue
                dep_path = self._locate(dep)
                resolved[dep] = dep_path
                frontier.append(dep)
        return resolved
