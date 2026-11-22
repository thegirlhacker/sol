"""Assemble the install tree from a resolved package set.

Each resolved package's payload is copied into `<out>/site-packages/<name>/`. The build config
(`build.json`) lists the top-level roots, the lockfile, and the index search path.
"""
import json
import os
import shutil

from builder.index import Index
from builder.lockfile import load as load_lock
from builder.resolver import Resolver

ROOT = os.environ.get("BUILDER_ROOT", "/app")


def _abs(path):
    """Config paths are relative to the build root (BUILDER_ROOT, default /app)."""
    return path if os.path.isabs(path) else os.path.join(ROOT, path)


class Build:
    def __init__(self, cfg):
        self.roots = cfg["roots"]
        self.lock_path = _abs(cfg["lock"])
        self.index_paths = [_abs(p) for p in cfg["indexes"]]
        self.out = _abs(cfg["out"])

    @classmethod
    def load(cls, path):
        with open(path, encoding="utf-8") as fh:
            return cls(json.load(fh))

    def run(self):
        index = Index(self.index_paths)
        lock = load_lock(self.lock_path)
        resolved = Resolver(index, lock).resolve(self.roots)

        site = os.path.join(self.out, "site-packages")
        if os.path.isdir(site):
            shutil.rmtree(site)
        os.makedirs(site, exist_ok=True)
        for name, path in sorted(resolved.items()):
            dst = os.path.join(site, name)
            shutil.copytree(os.path.join(path, "payload"), dst)
        return sorted(resolved)
