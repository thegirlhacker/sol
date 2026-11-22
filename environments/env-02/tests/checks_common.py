"""Shared helpers for the env-02 grader: a content digest that matches builder.pkg.digest, but
computed over an already-installed directory (which *is* the payload)."""
import hashlib
import os


def hash_tree(root):
    """sha256 over every file under `root` (relpath + bytes, sorted). Matches the digest a
    package's payload hashes to, so an installed tree can be compared to a vouched digest."""
    if not os.path.isdir(root):
        return None
    files = []
    for base, _dirs, names in os.walk(root):
        for name in sorted(names):
            full = os.path.join(base, name)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            files.append((rel, full))
    h = hashlib.sha256()
    for rel, full in sorted(files):
        h.update(rel.encode("utf-8"))
        h.update(b"\0")
        try:
            with open(full, "rb") as fh:
                h.update(fh.read())
        except OSError:
            return None
        h.update(b"\0")
    return "sha256:" + h.hexdigest()


def site_packages_dirs(roots):
    """Every `site-packages` directory under the collected roots."""
    out = []
    for root in roots:
        if not os.path.isdir(root):
            continue
        for base, dirs, _files in os.walk(root):
            if os.path.basename(base) == "site-packages":
                out.append(base)
            # don't descend into huge vendored trees we don't care about
            dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
    return out
