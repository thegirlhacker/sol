import json, random, sys

def gen(seed, n):
    r = random.Random(seed)
    tagpool = ["eu", "us", "beta", "ga", "mobile", "web", "trial", "paid"]
    out = []
    for i in range(n):
        out.append({"id": f"{seed}-{i:05d}",
                    "value": r.randint(0, 10_000),
                    "tags": r.sample(tagpool, r.randint(0, 3))})
    return out

seed, n, path = sys.argv[1], int(sys.argv[2]), sys.argv[3]
json.dump(gen(seed, n), open(path, "w"), indent=0)
print("wrote", n, "records to", path)
