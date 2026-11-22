"""Package indexes: directories the resolver searches for a named package.

The configured indexes are searched **in order**. `find` returns the first package directory with
a given name; `find_all` returns every match across the search path, in order -- more than one
index can carry a package of the same name.
"""
import os


class Index:
    def __init__(self, roots):
        self.roots = [r for r in roots if r]

    def _is_pkg(self, path):
        return os.path.isdir(path) and os.path.isfile(os.path.join(path, "meta.json"))

    def find(self, name):
        """The first package directory named `name` across the search roots, or None."""
        for root in self.roots:
            cand = os.path.join(root, name)
            if self._is_pkg(cand):
                return cand
        return None

    def find_all(self, name):
        """Every package directory named `name`, in search order (may be empty)."""
        found = []
        for root in self.roots:
            cand = os.path.join(root, name)
            if self._is_pkg(cand):
                found.append(cand)
        return found
