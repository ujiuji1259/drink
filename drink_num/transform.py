import json
fn = "関西医科大学.json"
with open(fn, "r") as f:
    data = json.load(f)

save_data = {}
for d in data:
    date = d.pop("start")
    save_data[date] = d

with open(fn, "w") as f:
    json.dump(save_data, f, ensure_ascii=False)

