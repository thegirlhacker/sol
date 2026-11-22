"""Tiny, safe template renderer: `{{ key }}` substitution, no logic.

Templates live under the templates dir, one `.txt` per notification type, with a `Subject:`
first line followed by a blank line and the body.
"""
import os
import re

_FIELD = re.compile(r"{{\s*(\w+)\s*}}")


def render(templates_dir: str, name: str, context: dict) -> tuple[str, str]:
    """Return (subject, body) for template `name` filled from `context`."""
    with open(os.path.join(templates_dir, name + ".txt"), encoding="utf-8") as fh:
        raw = fh.read()
    subject_line, _, body = raw.partition("\n\n")
    subject = subject_line.split("Subject:", 1)[1].strip() if "Subject:" in subject_line \
        else subject_line.strip()

    def sub(m):
        return str(context.get(m.group(1), m.group(0)))

    return _FIELD.sub(sub, subject), _FIELD.sub(sub, body)
