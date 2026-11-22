import json, os, random, sys

ENV, FIX = sys.argv[1], sys.argv[2]

def queue(seed, n):
    r = random.Random(seed)
    names = ["Ava", "Ben", "Chen", "Diya", "Ebru", "Finn", "Gita", "Hugo", "Ivy", "Jun"]
    out = []
    for i in range(n):
        name = r.choice(names)
        code = "".join(r.choice("0123456789") for _ in range(6))
        out.append({
            "id": f"{seed}-{i:03d}",
            "to": f"{name.lower()}{i}@customer.test",
            "type": "password_reset",
            "context": {"brand": "Northwind", "name": name, "code": code},
        })
    return {"notifications": out}

os.makedirs(os.path.join(ENV, "data"), exist_ok=True)
os.makedirs(FIX, exist_ok=True)
json.dump(queue("vis", 6), open(os.path.join(ENV, "data", "queue.json"), "w"), indent=2)
json.dump(queue("hid", 7), open(os.path.join(FIX, "queue.json"), "w"), indent=2)
# Hidden: the domains the service is authorised to send as (its own).
json.dump({"authorized": ["sandbox.northwind.test", "northwind.test"]},
          open(os.path.join(FIX, "authorized_domains.json"), "w"), indent=2)
print("wrote visible queue (6), hidden queue (7), authorized_domains")
