"""The taskr subcommands. Each takes the remaining argv and returns a line to print.

Tasks live in a JSON file; `login` opens a session. These are ordinary commands."""
import json
import os


def _tasks_path():
    root = os.environ.get("TASKR_ROOT", "/app")
    return os.environ.get("TASKR_TASKS", os.path.join(root, "var", "tasks.json"))


def _load():
    try:
        with open(_tasks_path(), encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {"tasks": []}


def _save(data):
    p = _tasks_path()
    os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(data, fh)


def cmd_add(args):
    data = _load()
    data["tasks"].append({"text": " ".join(args), "done": False})
    _save(data)
    return f"added task #{len(data['tasks'])}"


def cmd_list(args):
    data = _load()
    return "\n".join(f"{i+1}. [{'x' if t['done'] else ' '}] {t['text']}"
                     for i, t in enumerate(data["tasks"])) or "no tasks"


def cmd_done(args):
    data = _load()
    n = int(args[0]) if args and args[0].isdigit() else 0
    if 1 <= n <= len(data["tasks"]):
        data["tasks"][n - 1]["done"] = True
        _save(data)
        return f"done #{n}"
    return "no such task"


def cmd_login(args):
    # --token <value>: records that a session was opened.
    token = ""
    if "--token" in args:
        i = args.index("--token")
        token = args[i + 1] if i + 1 < len(args) else ""
    return "logged in" if token else "login requires --token"


COMMANDS = {"add": cmd_add, "list": cmd_list, "done": cmd_done, "login": cmd_login}
