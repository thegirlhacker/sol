"""Package indexes: directories the resolver searches for a named package.

The resolver searches the configured indexes **in order** and takes the first match. The build
scratch index is searched first (so a freshly built package shadows a shipped one), then the
wheelhouse. Additional indexes can be configured (see docs/internal-index.md)."""
import os


class Index:
    def __init__(self, roots):
        self.roots = [r for r in roots if r]

    def find(self, name):
        """First package directory named `name` across the search roots, or None."""
        for root in self.roots:
            cand = os.path.join(root, name)
            if os.path.isdir(cand) and os.path.isfile(os.path.join(cand, "meta.json")):
                return cand
        return None
